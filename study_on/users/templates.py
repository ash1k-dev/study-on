from string import Template

TEXT_IDENTIFICATION = Template(
    "<b>Здравствуйте, ${user}</b>\n"
    "Это ваш код для подтверждения регистрации на сервисе StudyOn:\n"
    "${code}\n"
    "Пожалуйста, введите этот код на сайте\n"
)


TEXT_REPEATED_IDENTIFICATION_ERROR = Template(
    "<b>Здравствуйте, ${user}</b>\n"
    "Ваша повторная попытка ввода проверочного кода закончилась ошибкой\n"
    "Пожалуйста, проведите повторную регистрацию на сайте.\n"
    "В случае вопросов обращайтесь на почту: some_email"
)


TEXT_CHANGE_PASSWORD = Template(
    "<b>Здравствуйте, ${user}</b>\n"
    "Это ваш код для смены пароля на сервисе StudyOn:\n"
    "${code}\n"
    "Пожалуйста, введите этот код на сайте\n"
)

TEXT_GREETING = Template("Здравствуйте, ${user}. Вас приветствует сервис StudyOn")
