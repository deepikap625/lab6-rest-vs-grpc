#!/usr/bin/env python3

import argparse
import base64
import io
from concurrent import futures

import grpc
from PIL import Image

import lab6_pb2
import lab6_pb2_grpc


class Lab6Service(lab6_pb2_grpc.Lab6ServiceServicer):

    def Add(self, request, context):
        return lab6_pb2.AddReply(sum=request.a + request.b)

    def RawImage(self, request, context):
        try:
            img = Image.open(io.BytesIO(request.img))
            return lab6_pb2.ImageReply(
                width=img.width,
                height=img.height
            )
        except Exception as e:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(e))

    def DotProduct(self, request, context):
        if len(request.a) != len(request.b):
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "Vectors must have the same length"
            )

        result = sum(a * b for a, b in zip(request.a, request.b))
        return lab6_pb2.DotProductReply(dotproduct=result)

    def JsonImage(self, request, context):
        try:
            image_bytes = base64.b64decode(request.img, validate=True)
            img = Image.open(io.BytesIO(image_bytes))

            return lab6_pb2.ImageReply(
                width=img.width,
                height=img.height
            )
        except Exception as e:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(e))


def serve(port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    lab6_pb2_grpc.add_Lab6ServiceServicer_to_server(
        Lab6Service(),
        server
    )

    server.add_insecure_port(f"[::]:{port}")
    server.start()

    print(f"gRPC server listening on port {port}")

    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Lab 6 gRPC server")
    parser.add_argument("-p", "--port", type=int, default=50051)
    args = parser.parse_args()

    serve(args.port)
