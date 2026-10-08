"""A chat model that answers instantly, with no download.

A test plugin for the dashAI plugin store: it reuses dashAI's own components
under other names. Display names end in "(plugin)" to tell them apart.
"""

import pyjokes

from DashAI.back.core.schema_fields import BaseSchema, int_field, schema_field
from DashAI.back.core.utils import MultilingualString
from DashAI.back.models.text_to_text_generation_model import (
    TextToTextGenerationTaskModel,
)
from DashAI.back.tasks.text_to_text_generation_task import TextToTextGenerationTask


class EchoChatTask(TextToTextGenerationTask):
    DISPLAY_NAME = MultilingualString(en="Echo chat (plugin)", es="Chat eco (plugin)")


class EchoSchema(BaseSchema):
    repeat: schema_field(
        int_field(ge=1, le=5),
        placeholder=1,
        description=MultilingualString(
            en="How many times the last message is repeated.",
            es="Cuántas veces se repite el último mensaje.",
        ),
        alias=MultilingualString(en="Repeat", es="Repeticiones"),
    )  # type: ignore


class EchoModel(TextToTextGenerationTaskModel):
    """Repeats the last user message; "/joke" answers with a joke."""

    COMPATIBLE_COMPONENTS = ["EchoChatTask"]
    SCHEMA = EchoSchema
    DISPLAY_NAME = MultilingualString(en="Echo (plugin)", es="Eco (plugin)")

    def __init__(self, **kwargs):
        self.repeat = kwargs.get("repeat", 1)

    def generate(self, input):
        last = input[-1]["content"] if isinstance(input, list) else str(input)
        if last.strip() == "/joke":
            return [pyjokes.get_joke()]
        return [" ".join([f"echo: {last}"] * self.repeat)]
