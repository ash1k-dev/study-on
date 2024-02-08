from string import Template

TEXT_REMINDER = Template(
    "<b>Здравствуйте, ${student}</b>\n"
    "Вы давно не посещали курс ${course_name}\n"
    "Не потеряйте свой прогресс, успех в обучении всегода приходит при регулярных занятиях\n"
    "Возвращайтесь, мы Вас ждем!"
)

TEXT_GREETING = Template("Здравствуйте, ${student}. Ваш курс ждет Вас!\n")
