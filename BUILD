load("@com_github_grpc_grpc//bazel:python_rules.bzl", "py_proto_library")
load("@rules_proto//proto:defs.bzl", "proto_library")
load("@subpar//:subpar.bzl", "par_binary")

proto_library(
    name = "goto_proto",
    srcs = ["goto.proto"],
    deps = [],
)

py_proto_library(
    name = "goto_py_proto",
    deps = [
        ":goto_proto",
    ],
)
