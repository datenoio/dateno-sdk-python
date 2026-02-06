from __future__ import annotations

import httpx

from .types import BeforeRequestContext, BeforeRequestHook, Hooks


# This file is only ever generated once on the first generation and then is free to be modified.
# Any hooks you wish to add should be registered in the init_hooks function. Feel free to define them
# in this file or in separate files in the hooks folder.


class _DatenoClientHeaderHook(BeforeRequestHook):
    def before_request(
        self, hook_ctx: BeforeRequestContext, request: httpx.Request
    ) -> httpx.Request:
        header_name = "Dateno-Client"
        if header_name in request.headers:
            return request
        version = getattr(hook_ctx.config, "sdk_version", None) or "unknown"
        request.headers[header_name] = f"sdk-python/{version}"
        return request


def init_hooks(hooks: Hooks):
    # pylint: disable=unused-argument
    """Add hooks by calling hooks.register{sdk_init/before_request/after_success/after_error}Hook
    with an instance of a hook that implements that specific Hook interface
    Hooks are registered per SDK instance, and are valid for the lifetime of the SDK instance"""
    hooks.register_before_request_hook(_DatenoClientHeaderHook())
