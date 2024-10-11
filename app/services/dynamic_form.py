from typing import Any, Dict, List, Optional, Type, Union, get_args, get_origin, Tuple
from nicegui import ui
from enum import Enum


class TypeMapper:
    UI_TYPES = {str: ui.input, int: ui.number, bool: ui.checkbox}

    TYPE_HANDLERS = {
        list: lambda args: ui.select if isinstance(args[0], type) and issubclass(args[0], Enum) else ui.input,
        dict: lambda args: "dict",
        Enum: lambda _: ui.select,
        Union: lambda args: TypeMapper.map_non_none(args),
    }

    @staticmethod
    def map_string_to_enum(enum_class: Type[Enum], value: str) -> Optional[Enum]:
        if not value or not enum_class:
            return None
        try:
            return enum_class[value]
        except KeyError:
            print(f"Failed to map '{value}' to an enum member of {enum_class.__name__}")
            return None

    @staticmethod
    def map(python_type: Any) -> Any:
        origin = get_origin(python_type)
        args = get_args(python_type)
        if origin in TypeMapper.TYPE_HANDLERS:
            return TypeMapper.TYPE_HANDLERS[origin](args)
        return TypeMapper.UI_TYPES.get(python_type, ui.input)

    @staticmethod
    def map_non_none(args: Tuple[Any, ...]) -> Any:
        non_none_args = [arg for arg in args if arg is not type(None)]
        return TypeMapper.map(non_none_args[0]) if non_none_args else ui.input

    @staticmethod
    def _map_value_to_type(value, python_type):
        if value is None:
            return None
        if isinstance(value, tuple):
            value = value[0]
        if isinstance(python_type, type) and issubclass(python_type, Enum):
            result = python_type.__members__.get(value)
            if result:
                return result
            return TypeMapper.map_string_to_enum(python_type, value)
        elif python_type is int:
            try:
                return int(value)
            except ValueError:
                print(f"Failed to convert '{value}' to int")
                return None
        elif python_type is float:
            try:
                return float(value)
            except ValueError:
                print(f"Failed to convert '{value}' to float")
                return None
        return value

    @staticmethod
    def get_enum_options(enum_class: Type[Enum]) -> Dict[str, str]:
        if not enum_class:
            return {"None": None}
        return {e.name: e.value for e in enum_class}

    @classmethod
    def create_extras(cls, python_type: Any) -> Dict[str, Any]:
        extras = {}
        origin = get_origin(python_type)
        args = get_args(python_type)
        if origin is list and args:
            extras["multiple"] = True
            item_type = args[0]
            if isinstance(item_type, type) and issubclass(item_type, Enum):
                extras["options"] = cls.get_enum_options(item_type)
        elif origin is dict and len(args) == 2:
            extras["multiple_fields"] = True
            key_type, value_type = args
            extras["key_type"] = key_type
            extras["value_type"] = value_type
        elif isinstance(python_type, type) and issubclass(python_type, Enum):
            extras["options"] = cls.get_enum_options(python_type)
        return extras


class DynamicField:
    def __init__(self, name: str, label: str, field_type: Any, extras: Dict[str, Any] = None, original_type: Any = None):
        self.name = name
        self.label = label
        self.field_type = field_type
        self.extras = extras or {}
        self.key_value_fields = []
        self.original_type = original_type
        self.ui_field = None
        self.field_container = None

    def create_ui_component(self, is_key_value_pair: bool = False) -> Any:
        if self.field_type == "dict" and self.extras.get("multiple_fields", False):
            self.field_container = ui.column().classes("w-full")
            ui.button("Add Pair", on_click=lambda: self.add_key_value_pair()).classes("w-full")
            return self.field_container

        options = self.extras.get("options", {})
        multiple = self.extras.get("multiple", False)

        if options:
            component = ui.select(options=options, label=self.label, multiple=multiple)
            if multiple:
                component.props("use-chips")
        else:
            component = TypeMapper.map(self.field_type)(label=self.label)

        component.classes("w-1/2" if is_key_value_pair else "w-full")
        self.ui_field = component
        return component

    def add_key_value_pair(self):
        key_type = self.extras.get("key_type", str)
        value_type = self.extras.get("value_type", str)
        with self.field_container:
            with ui.row().classes("w-full"):
                key_field = self._create_field_component(key_type, f"{self.label} Key")
                value_field = self._create_field_component(value_type, f"{self.label} Value")
                self.key_value_fields.append((key_field, value_field))

    def _create_field_component(self, field_type: Any, label: str) -> Any:
        if isinstance(field_type, type) and issubclass(field_type, Enum):
            options = TypeMapper.get_enum_options(field_type)
            field = ui.select(options=options, label=label).classes("w-1/2")
        else:
            field_type_ui = TypeMapper.map(field_type)
            field = field_type_ui(label=label).classes("w-1/2")
        return field


class DynamicForm:
    def __init__(self, form_container: Any, submit_callback: Any, object_name: str = "Object", excluded_fields: List[str] = None):
        self.form_container = form_container
        self.submit_callback = submit_callback
        self.object_name = object_name
        self.excluded_fields = excluded_fields or []
        self.fields = []
        self.fields_container = ui.column().classes("w-full")
        self.button_container = ui.column().classes("w-full")
        self.submit_button = ui.button(f"Create {self.object_name}", on_click=self.submit_form).classes("w-full")
        self.field_widgets = {}

    def create_form(self, object_class: Any) -> None:
        self.form_container.clear()
        self.fields = []
        self.fields_container.clear()
        fields = self.extract_fields_from_class(object_class)
        with self.form_container:
            self.fields_container
            self.button_container
        with self.fields_container:
            for field in fields:
                self.add_field(field)
        with self.button_container:
            self.submit_button

    def extract_fields_from_class(self, object_class: Any) -> List[DynamicField]:
        fields = []
        for cls in reversed(object_class.__mro__):
            if cls is object:
                continue
            annotations = getattr(cls, "__annotations__", {})
            for attr, attr_type in annotations.items():
                if attr in self.excluded_fields:
                    continue
                label = attr.replace("_", " ").capitalize()
                is_optional = False
                origin = get_origin(attr_type)
                if origin is Union and type(None) in get_args(attr_type):
                    is_optional = True
                    attr_type = [arg for arg in get_args(attr_type) if arg is not type(None)][0]
                field_type = TypeMapper.map(attr_type)
                extras = TypeMapper.create_extras(attr_type)
                if is_optional:
                    label += " (Optional)"
                fields.append(DynamicField(attr, label, field_type, extras, original_type=attr_type))
        return fields

    def add_field(self, field: DynamicField) -> None:
        ui_field = field.create_ui_component()
        with self.fields_container:
            ui_field
        self.field_widgets[field.name] = ui_field
        self.fields.append(field)

    def submit_form(self) -> None:
        form_data = {}
        for field in self.fields:
            if not field.extras.get("multiple_fields", False):
                form_data[field.name] = self._convert_value(field, field.ui_field.value)
            else:
                dict_data = {}
                for key_input, value_input in field.key_value_fields:
                    key = self._convert_value_field(key_input, field.extras.get("key_type"))
                    value = self._convert_value_field(value_input, field.extras.get("value_type"))
                    if key is not None and value is not None:
                        dict_data[key] = value
                form_data[field.name] = dict_data
        self.submit_callback(form_data)

    def _convert_value(self, field: DynamicField, value: Any) -> Any:
        return TypeMapper._map_value_to_type(value, field.original_type)

    def _convert_value_field(self, ui_field, python_type):
        value = ui_field.value
        return TypeMapper._map_value_to_type(value, python_type)


class EditDynamicForm(DynamicForm):
    def __init__(self, form_container: Any, submit_callback: Any, existing_object: Any, object_name: str = "Object", excluded_fields: List[str] = None):
        super().__init__(form_container, submit_callback, object_name, excluded_fields)
        self.existing_object = existing_object

    def create_form(self) -> None:
        object_class = type(self.existing_object)
        super().create_form(object_class)
        self.populate_fields_with_existing_values()

    def populate_fields_with_existing_values(self) -> None:
        for field in self.fields:
            field_widget = field.ui_field
            existing_value = getattr(self.existing_object, field.name, None)
            field_type = field.original_type
            if isinstance(field_type, type) and issubclass(field_type, Enum):
                if hasattr(field_widget, "options"):
                    field_widget.options = {e.name: e.name for e in field_type}
                    if isinstance(existing_value, Enum):
                        field_widget.value = existing_value.name
                    elif isinstance(existing_value, str):
                        enum_value = TypeMapper.map_string_to_enum(field_type, existing_value)
                        if enum_value:
                            field_widget.value = enum_value.name
                        else:
                            field_widget.value = existing_value
                    else:
                        field_widget.value = None
                    field_widget.update()
            elif get_origin(field_type) is dict:
                field.key_value_fields = []
                field.field_container.clear()
                if existing_value:
                    for key, value in existing_value.items():
                        field.add_key_value_pair()
                        key_input, value_input = field.key_value_fields[-1]
                        if isinstance(key, Enum):
                            key_input.options = {e.name: e.name for e in type(key)}
                            key_input.value = key.name
                        else:
                            key_input.value = key
                        key_input.update()
                        if isinstance(value, Enum):
                            value_input.options = {e.name: e.name for e in type(value)}
                            value_input.value = value.name
                        else:
                            value_input.value = value
                        value_input.update()
            elif existing_value is not None:
                if isinstance(existing_value, float) and field_type is int:
                    existing_value = int(existing_value)
                field_widget.value = existing_value
                field_widget.update()
