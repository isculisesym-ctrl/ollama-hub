"""Tests for validation logic"""

import pytest
from fastapi import HTTPException

from app.utils import (
    validate_project_name,
    validate_message,
    validate_model_name,
    validate_api_key,
    safe_json_parse,
)


class TestValidation:
    def test_validate_project_name_valid(self):
        result = validate_project_name("My Project")
        assert result == "My Project"

    def test_validate_project_name_empty(self):
        with pytest.raises(HTTPException) as exc:
            validate_project_name("")
        assert exc.value.status_code == 422

    def test_validate_project_name_whitespace(self):
        with pytest.raises(HTTPException):
            validate_project_name("   ")

    def test_validate_project_name_too_long(self):
        with pytest.raises(HTTPException) as exc:
            validate_project_name("x" * 201)
        assert exc.value.status_code == 422

    def test_validate_message_valid(self):
        result = validate_message("Hello world")
        assert result == "Hello world"

    def test_validate_message_empty(self):
        with pytest.raises(HTTPException):
            validate_message("")

    def test_validate_message_too_long(self):
        with pytest.raises(HTTPException):
            validate_message("x" * 50001)

    def test_validate_model_name_valid(self):
        result = validate_model_name("llama3")
        assert result == "llama3"

    def test_validate_model_name_empty(self):
        with pytest.raises(HTTPException):
            validate_model_name("")

    def test_validate_api_key_valid(self):
        result = validate_api_key("sk-1234567890")
        assert result == "sk-1234567890"

    def test_validate_api_key_too_short(self):
        with pytest.raises(HTTPException):
            validate_api_key("short")

    def test_safe_json_parse_valid(self):
        result = safe_json_parse('{"key": "value"}')
        assert result["key"] == "value"

    def test_safe_json_parse_invalid(self):
        result = safe_json_parse("invalid json")
        assert result == {}

    def test_safe_json_parse_empty(self):
        result = safe_json_parse("")
        assert result == {}

    def test_safe_json_parse_with_default(self):
        result = safe_json_parse("invalid", {"default": True})
        assert result["default"] is True
