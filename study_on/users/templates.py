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

TEXT_REWARD = Template(
    "<b>Здравствуйте, ${user}</b>\n"
    "Вы получили награду на сервисе StudyOn:\n"
    "${reward}\n"
    "Все ваши награды можно посмотреть в профиле\n"
)


TEXT_SURVEY_APPROVE = Template(
    "<b>Здравствуйте, ${user}</b>\n"
    "Ваши ответы на задание к уроку ${lesson} были проверены.\n"
    "Вы отлично справились с заданием и можете приступить к следующему уроку\n"
)


TEXT_SURVEY_DONE = Template(
    "<b>Здравствуйте, ${user}</b>\n"
    "Студент ответил на все вопросы к уроку ${lesson}.\n"
    "Вы можете приступить к проверке\n"
)

TEXT_GREETING = Template("Здравствуйте, ${user}. Вас приветствует сервис StudyOn")
