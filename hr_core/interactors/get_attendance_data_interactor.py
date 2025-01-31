from typing import List

from django.http import HttpResponse

from hr_core.exceptions.custom_exceptions import InvalidEmployeeId
from hr_core.exceptions.custom_exceptions import InvalidMonth
from hr_core.exceptions.custom_exceptions import InvalidYear
from hr_core.interactors.presenter_interfaces.presenter_interface import (
    PresenterInterface,
)
from hr_core.interactors.storage_interfaces.dtos import AttendanceDTO
from hr_core.interactors.storage_interfaces.dtos import AttendanceParamDTO
from hr_core.interactors.storage_interfaces.storage_interface import StorageInterface


class GetAttendanceDataInteractor:

    def __init__(self, storage: StorageInterface):
        self.storage = storage

    def get_attendance_data_wrapper(
        self, attendance_params: AttendanceParamDTO, presenter: PresenterInterface
    ) -> HttpResponse:
        try:
            attendance_data_dto_list = self.get_attendance_data(
                attendance_params=attendance_params
            )
        except InvalidMonth:
            return presenter.raise_exception_for_invalid_month()
        except InvalidYear:
            return presenter.raise_exception_for_invalid_year()
        except InvalidEmployeeId:
            return presenter.raise_exception_for_invalid_employee()

        return presenter.get_response_for_get_attendance_data(
            attendance_dto_list=attendance_data_dto_list
        )

    def get_attendance_data(self, attendance_params: AttendanceParamDTO) -> List[AttendanceDTO]:
        self._validate_month(month=attendance_params.month)
        self._validate_year(year=attendance_params.year)
        self.storage.validate_employee_id(employee_id=attendance_params.employee_id)

        attendance_data_dtos = self.storage.get_attendance_data_for_month_year_dto(
            attendance_params=attendance_params)
        return attendance_data_dtos

    @staticmethod
    def _validate_month(month: int) -> None:
        is_month_valid = 1 <= month <= 12
        is_month_not_valid = not is_month_valid

        if is_month_not_valid:
            raise InvalidMonth(month=month)

    @staticmethod
    def _validate_year(year: int) -> None:
        from datetime import date
        current_year = date.today().year
        is_year_valid = year <= current_year
        is_year_not_valid = not is_year_valid

        if is_year_not_valid:
            raise InvalidYear(year=year)
