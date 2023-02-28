from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, OpenApiExample
from rest_framework import status

DATE_PARAMETER = OpenApiParameter(
    name='date',
    description='Дата начала действия в формате ГГГГ-ММ-ДД. </br>'
                'Если указана, то должны возвратиться только те справочники, '
                'в которых имеются Версии с Датой начала действия раннее '
                'или равной указанной.',
    required=False,
    type=OpenApiTypes.DATE,
)

VERSION_PARAMETER = OpenApiParameter(
    name='version',
    description='Версия справочника. </br>Если не указана, '
                'то должны возвращаться элементы текущей версии.'
                'Текущей является та версия, дата начала действия которой '
                'позже всех остальных версий данного справочника, '
                'но не позже текущей даты.',
    required=False,
    type=OpenApiTypes.STR,
)

CODE_PARAMETER = OpenApiParameter(
    name='code',
    description='Код элемента справочника',
    required=True,
    type=OpenApiTypes.STR,
)

VALUE_PARAMETER = OpenApiParameter(
    name='value',
    description='Значение элемента справочника',
    required=True,
    type=OpenApiTypes.STR,
)

REFBOOKS_OK_EXAMPLE = OpenApiExample(
    'OK',
    value={
        "refbooks": [
            {
                "id": "1",
                "code": "MS1",
                "name": " "
            },
            {
                "id": "2",
                "code": "ICD-10",
                "name": " -10"
            },
        ]
    },
    status_codes=[status.HTTP_200_OK],
    response_only=True,
)

REFBOOKS_BAD_REQUEST_EXAMPLE = OpenApiExample(
    'Bad request',
    summary='Ошибка отправки данных',
    description='Неправильный формат date. Используйте один из этих форматов: YYYY-MM-DD.',
    value={
        'date': "Неправильный формат date. Используйте один из этих форматов: YYYY-MM-DD.",
    },
    status_codes=[status.HTTP_400_BAD_REQUEST],
    response_only=True,

)
ELEMENTS_LIST_OK_EXAMPLE = OpenApiExample(
    'OK',
    value={
        "elements": [
            {
                "code": "J00",
                "value": " ()"
            },
            {
                "code": "J01",
                "value": " "
            }
        ]
    },
    status_codes=[status.HTTP_200_OK],
    response_only=True,
)

ELEMENTS_LIST_BAD_REQUEST_EXAMPLE = OpenApiExample(
    'Bad request',
    summary='Ошибка отправки данных',
    description="Убедитесь, что это значение содержит не более 50 символов.",
    value={
        "version": [
            "Убедитесь, что это значение содержит не более 50 символов."
        ]
    },
    status_codes=[status.HTTP_400_BAD_REQUEST],
    response_only=True,
)

ELEMENT_VALIDATION_EXISTS_EXAMPLE = OpenApiExample(
    'Присутствует',
    value={
        "exists": True,
    },
    status_codes=[status.HTTP_200_OK],
    response_only=True,
)

ELEMENT_VALIDATION_NOT_EXISTS_EXAMPLE = OpenApiExample(
    'Отсутствует',
    value={
        "exists": False,
    },
    status_codes=[status.HTTP_200_OK],
    response_only=True,
)

ELEMENT_VALIDATION_CODE_ERROR_EXAMPLE = OpenApiExample(
    'Ошибка code',
    summary='Ошибка code',
    value={
        "code": [
            "Обязательное поле."
        ]
    },
    status_codes=[status.HTTP_400_BAD_REQUEST],
    response_only=True,
)

ELEMENT_VALIDATION_VALUE_ERROR_EXAMPLE = OpenApiExample(
    'Ошибка value',
    summary='Ошибка value',
    value={
        "value": [
            "Обязательное поле."
        ]
    },
    status_codes=[status.HTTP_400_BAD_REQUEST],
    response_only=True,
)

ELEMENT_VALIDATION_VERSION_ERROR_EXAMPLE = OpenApiExample(
    'Ошибка version',
    summary='Ошибка version',
    value={
        "version": [
            "Убедитесь, что это значение содержит не более 50 символов."
        ]
    },
    status_codes=[status.HTTP_400_BAD_REQUEST],
    response_only=True,
)
