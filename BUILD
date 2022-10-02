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

par_binary(
    name = "generate_links",
    srcs = ["generate_links.py"],
    python_version = "PY3",
    deps = [
        ":goto_py_proto",
        "@abseil//absl:app",
        "@abseil//absl/flags",
        "@abseil//absl/logging",
    ],
)

py_test(
    name = "generate_links_test",
    srcs = ["generate_links_test.py"],
    python_version = "PY3",
    deps = [
        ":generate_links",
        ":goto_py_proto",
        "@abseil//absl/testing:absltest",
        "@abseil//absl/testing:flagsaver",
        "@abseil//absl/testing:parameterized",
        "@rules_python//python/runfiles",
    ],
)
