from datetime import datetime, timezone
from pydantic import BaseModel, Extra, validator
from pydantic.error_wrappers import ErrorWrapper, ValidationError
from pydantic.errors import ConfigError, ExtraError, MissingError
from pydantic.utils import ROOT_KEY, GetterDict
from pydantic import root_validator
from typing import Any
from app.logger import Logger

logger = Logger.get_logger()


class BaseSchema(BaseModel):
    """Base Schema."""

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

    @validator("*")
    def datetime_format(cls, value):
        if isinstance(value, datetime):
            value = value.replace(tzinfo=timezone.utc)
        return value

    @classmethod
    def from_orm(cls, obj):
        """Parse obj from ORM."""

        try:
            obj_copy = obj
            object_setattr = object.__setattr__
            if not cls.__config__.orm_mode:
                raise ConfigError('You must have the config attribute orm_mode=True to use from_orm')
            obj = {ROOT_KEY: obj} if cls.__custom_root_type__ else cls._decompose_class(obj)
            m = cls.__new__(cls)
            values, fields_set, validation_error = cls.validate_model(cls, obj)
            if validation_error:
                raise validation_error
            object_setattr(m, '__dict__', values)
            object_setattr(m, '__fields_set__', fields_set)
            m._init_private_attributes()
            return m
        except Exception as ex:
            cls._handle_error(obj_copy, ex)
            return ex

    @staticmethod
    def validate_model(model, input_data, cls=None):
        """Validate data against a model."""

        values = {}
        errors = []
        names_used = set()
        fields_set = set()
        config = model.__config__
        check_extra = config.extra is not Extra.ignore
        cls_ = cls or model

        for _validator in model.__pre_root_validators__:
            try:
                input_data = _validator(cls_, input_data)
            except (ValueError, TypeError, AssertionError) as exc:
                return {}, set(), ValidationError([ErrorWrapper(exc, loc=ROOT_KEY)], cls_)

        _missing = object()
        for name, field in model.__fields__.items():
            value = input_data.get(field.alias, _missing)
            using_name = False
            if value is _missing and config.allow_population_by_field_name and field.alt_alias:
                value = input_data.get(field.name, _missing)
                using_name = True

            if value is _missing:
                if field.required:
                    errors.append(ErrorWrapper(MissingError(), loc=field.alias))
                    continue

                value = field.get_default()

                if not config.validate_all and not field.validate_always:
                    values[name] = value
                    continue
            else:
                fields_set.add(name)
                if check_extra:
                    names_used.add(field.name if using_name else field.alias)

            v_, errors_ = field.validate(value, values, loc=field.alias, cls=cls_)
            if isinstance(errors_, ErrorWrapper):
                errors.append(errors_)
            elif isinstance(errors_, list):
                errors.extend(errors_)
            else:
                values[name] = v_

        if check_extra:
            if isinstance(input_data, GetterDict):
                extra = input_data.extra_keys() - names_used
            else:
                extra = input_data.keys() - names_used
            if extra:
                fields_set |= extra
                if config.extra is Extra.allow:
                    for f in extra:
                        values[f] = input_data[f]
                else:
                    errors.extend(ErrorWrapper(ExtraError(), loc=f) for f in sorted(extra))
        for skip_on_failure, _validator in model.__post_root_validators__:
            if skip_on_failure and errors:
                continue
            try:
                values = _validator(cls_, values)
            except (ValueError, TypeError, AssertionError) as exc:
                logger.exception(exc)
                errors.append(ErrorWrapper(exc, loc=ROOT_KEY))

        if errors:
            return values, fields_set, ValidationError(errors, cls_)
        else:
            return values, fields_set, None

    @classmethod
    def _handle_error(cls, object, ex):
        """Handle Schema parsing error."""

        try:
            object_dict = cls._parse_obj_to_dict(object)
            logger.exception(f"Error on parsing schema {object_dict}: {ex}")
        except Exception as exc:
            logger.exception(f"Error on handling error parsing schema {object}: {ex} | {exc}")
        raise ex

    @staticmethod
    def _parse_obj_to_dict(object):
        """Parse schema obj/objs to dict/list."""

        objs = object
        if not isinstance(object, list):
            objs = [object]
        object_dicts = []

        for obj in objs:
            obj_dict = obj.__dict__
            for key, value in obj_dict.items():
                if isinstance(value, list):
                    temp_list = [v.__dict__ for v in value]
                    obj_dict[key] = temp_list
            object_dicts.append(obj_dict)

        return object_dicts


class BaseRequestSchema(BaseSchema):
    """Base Schema for Request."""

    pass


class BaseResponseSchema(BaseSchema):
    """Base Schema for Response."""

    status: str
    data: Any

    class Config:
        orm_mode = True

    @root_validator(pre=True)
    def format(cls, values):

        data = values
        if not isinstance(values, dict):
            data = values._obj

        return {
            'status': 'success', 
            'data': data
        }
