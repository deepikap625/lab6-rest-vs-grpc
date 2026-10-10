#!/usr/bin/env python3

import argparse
import base64
import random
import time

import grpc

import lab6_pb2
import lab6_pb2_grpc


def main():
    parser = argparse.ArgumentParser(
        description="gRPC client for measuring Lab 6 operations"
    )

    parser.add_argument("host", help="gRPC server hostname or IP")
    parser.add_argument(
        "cmd",
        choices=["add", "rawImage", "dotProduct", "jsonImage"],
        help="Operation to perform"
    )
    parser.add_argument("reps", type=int, help="Number of repetitions")
    parser.add_argument("-p", "--port", type=int, default=50051)
    parser.add_argument("-d", "--debug", action="store_true")

    args = parser.parse_args()

    if args.reps <= 0:
        parser.error("reps must be greater than zero")

    address = f"{args.host}:{args.port}"
    print(f"Running {args.reps} reps against {address}")

    # Read the image once, outside the timing loop.
    image_bytes = None
    encoded_image = None

    if args.cmd in ("rawImage", "jsonImage"):
        with open("Flatirons_Winter_Sunrise_edit_2.jpg", "rb") as f:
            image_bytes = f.read()

        encoded_image = base64.b64encode(image_bytes).decode("utf-8")

    # Generate the vectors once so all repetitions use the same input.
    if args.cmd == "dotProduct":
        vector_a = [random.random() for _ in range(100)]
        vector_b = [random.random() for _ in range(100)]

    with grpc.insecure_channel(address) as channel:
        stub = lab6_pb2_grpc.Lab6ServiceStub(channel)

        # Establish the connection before measuring repeated requests.
        grpc.channel_ready_future(channel).result(timeout=10)

        def call_operation():
            if args.cmd == "add":
                return stub.Add(
                    lab6_pb2.AddRequest(a=5, b=10)
                )

            if args.cmd == "rawImage":
                return stub.RawImage(
                    lab6_pb2.RawImageRequest(img=image_bytes)
                )

            if args.cmd == "dotProduct":
                return stub.DotProduct(
                    lab6_pb2.DotProductRequest(
                        a=vector_a,
                        b=vector_b
                    )
                )

            return stub.JsonImage(
                lab6_pb2.JsonImageRequest(img=encoded_image)
            )

        # Warm-up call, excluded from the timing.
        result = call_operation()

        start = time.perf_counter()

        for _ in range(args.reps):
            result = call_operation()

        elapsed_ms = (
            (time.perf_counter() - start) / args.reps
        ) * 1000

        if args.debug:
            print("Response:", result)

        print(f"Took {elapsed_ms:.3f} ms per operation")


if __name__ == "__main__":
    main()
