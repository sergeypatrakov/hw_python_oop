from typing import Dict, Type
from dataclasses import asdict, dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    MESSAGE: str = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )

    def get_message(self) -> str:
        """Итоги тренировки"""
        return self.MESSAGE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    TIME_IN_MINUTES: int = 60

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
    ) -> None:
        self.action: int = action
        self.duration: float = duration
        self.weight: float = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        # return type(InfoMessage)
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""
    COEFF_CALORIE_1: int = 18
    COEFF_CALORIE_2: int = 20

    def get_spent_calories(self) -> float:
        return (
            (self.COEFF_CALORIE_1
             * self.get_mean_speed()
             - self.COEFF_CALORIE_2)
            * self.weight
            / self.M_IN_KM
            * (self.duration
               * self.TIME_IN_MINUTES)
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    COEFF_CALORIE_WLK_1: float = 0.035
    COEFF_CALORIE_WLK_2: float = 0.029

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        height: float
    ) -> None:
        super().__init__(
            action,
            duration,
            weight
        )
        self.height: float = height

    def get_spent_calories(self) -> float:
        return (
            (self.COEFF_CALORIE_WLK_1
             * self.weight
             + (self.get_mean_speed()**2
                // self.height)
             * self.COEFF_CALORIE_WLK_2
             * self.weight)
            * (self.duration
               * self.TIME_IN_MINUTES)
        )


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    COEFF_CALORIE_SWM_1: float = 1.1
    COEFF_CALORIE_SWM_2: float = 2

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        length_pool: float,
        count_pool: float
    ) -> None:
        super().__init__(
            action,
            duration,
            weight
        )
        self.length_pool: float = length_pool
        self.count_pool: float = count_pool

    def get_mean_speed(self) -> float:
        return (
            self.length_pool
            * self.count_pool
            / self.M_IN_KM
            / self.duration
        )

    def get_spent_calories(self) -> float:
        calories: float = (
            (self.get_mean_speed()
             + self.COEFF_CALORIE_SWM_1)
            * self.COEFF_CALORIE_SWM_2
            * self.weight
        )
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    WORKOUT_TYPES: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type in WORKOUT_TYPES:
        return WORKOUT_TYPES[workout_type](*data)
    else:
        raise ValueError('Такой вид тренировки не найден.')


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
