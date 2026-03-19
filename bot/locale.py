STRINGS: dict[str, dict[str, str]] = {
    "ru": {
        "choose_language": "Выберите язык / Choose language / Scegli la lingua:",
        "language_set": "Язык установлен: Русский 🇷🇺",
        "welcome": (
            "Привет! Я бот для отслеживания статуса permesso di soggiorno.\n\n"
            "Используйте кнопки ниже для управления."
        ),
        "help": (
            "📋 Как пользоваться:\n\n"
            "➕ <b>Добавить дело</b> — начать отслеживание по номеру\n"
            "📋 <b>Статус</b> — текущий статус всех дел\n"
            "🗑 <b>Удалить дело</b> — убрать дело из отслеживания\n"
            "🌐 <b>Язык</b> — сменить язык интерфейса\n\n"
            "Бот проверяет статус каждые 6 часов и уведомляет при изменениях."
        ),
        "btn_add": "➕ Добавить дело",
        "btn_status": "📋 Статус",
        "btn_remove": "🗑 Удалить дело",
        "btn_language": "🌐 Язык",
        "btn_help": "❓ Помощь",
        "btn_menu": "« Меню",
        "prompt_add": "Отправьте мне номер дела.\nПример: <code>26NA123456</code>",
        "prompt_remove": "Выберите дело для удаления:",
        "case_added": "✅ Дело <code>{case}</code> добавлено.\nТекущий статус: {status}",
        "case_exists": "⚠️ Дело <code>{case}</code> уже отслеживается.",
        "case_not_found": "❌ Дело <code>{case}</code> не найдено в архиве.",
        "case_removed": "✅ Дело <code>{case}</code> удалено из отслеживания.",
        "case_not_tracked": "⚠️ Дело <code>{case}</code> не найдено в вашем списке.",
        "status_header": "📋 Ваши дела:\n",
        "status_row": "{i}. <code>{case}</code> — {status}\n   <i>(проверено: {checked})</i>",
        "no_cases": "У вас нет отслеживаемых дел.",
        "status_changed": "🔔 Статус дела <code>{case}</code> изменился!\n\nНовый статус: {status}",
        "btn_check_website": "🌐 Проверить на сайте",
        "check_error": "⚠️ Не удалось проверить статус дела <code>{case}</code>.",
        "limit_reached": "⚠️ Достигнут лимит (10 дел). Сначала удалите ненужные.",
        "not_registered": "Пожалуйста, начните с /start для выбора языка.",
        "checking": "⏳ Проверяю дело <code>{case}</code>…",
    },
    "en": {
        "choose_language": "Выберите язык / Choose language / Scegli la lingua:",
        "language_set": "Language set: English 🇬🇧",
        "welcome": (
            "Hello! I'm a bot for tracking your permesso di soggiorno status.\n\n"
            "Use the buttons below to manage your cases."
        ),
        "help": (
            "📋 How to use:\n\n"
            "➕ <b>Add case</b> — start tracking by case number\n"
            "📋 <b>Status</b> — check current status of all cases\n"
            "🗑 <b>Remove case</b> — stop tracking a case\n"
            "🌐 <b>Language</b> — change interface language\n\n"
            "The bot checks status every 6 hours and notifies you of changes."
        ),
        "btn_add": "➕ Add case",
        "btn_status": "📋 Status",
        "btn_remove": "🗑 Remove case",
        "btn_language": "🌐 Language",
        "btn_help": "❓ Help",
        "btn_menu": "« Menu",
        "prompt_add": "Send me the case number.\nExample: <code>26NA123456</code>",
        "prompt_remove": "Choose a case to remove:",
        "case_added": "✅ Case <code>{case}</code> added.\nCurrent status: {status}",
        "case_exists": "⚠️ Case <code>{case}</code> is already being tracked.",
        "case_not_found": "❌ Case <code>{case}</code> not found in the archive.",
        "case_removed": "✅ Case <code>{case}</code> removed from tracking.",
        "case_not_tracked": "⚠️ Case <code>{case}</code> is not in your list.",
        "status_header": "📋 Your cases:\n",
        "status_row": "{i}. <code>{case}</code> — {status}\n   <i>(checked: {checked})</i>",
        "no_cases": "You have no tracked cases.",
        "status_changed": "🔔 Status of case <code>{case}</code> has changed!\n\nNew status: {status}",
        "btn_check_website": "🌐 Check on website",
        "check_error": "⚠️ Failed to check status of case <code>{case}</code>.",
        "limit_reached": "⚠️ Limit reached (10 cases). Remove some first.",
        "not_registered": "Please start with /start to choose a language.",
        "checking": "⏳ Checking case <code>{case}</code>…",
    },
    "it": {
        "choose_language": "Выберите язык / Choose language / Scegli la lingua:",
        "language_set": "Lingua impostata: Italiano 🇮🇹",
        "welcome": (
            "Ciao! Sono un bot per monitorare lo stato del permesso di soggiorno.\n\n"
            "Usa i pulsanti qui sotto per gestire le tue pratiche."
        ),
        "help": (
            "📋 Come usare:\n\n"
            "➕ <b>Aggiungi pratica</b> — inizia il monitoraggio per numero\n"
            "📋 <b>Stato</b> — controlla lo stato attuale di tutte le pratiche\n"
            "🗑 <b>Rimuovi pratica</b> — interrompi il monitoraggio\n"
            "🌐 <b>Lingua</b> — cambia la lingua dell'interfaccia\n\n"
            "Il bot controlla lo stato ogni 6 ore e ti avvisa in caso di modifiche."
        ),
        "btn_add": "➕ Aggiungi pratica",
        "btn_status": "📋 Stato",
        "btn_remove": "🗑 Rimuovi pratica",
        "btn_language": "🌐 Lingua",
        "btn_help": "❓ Aiuto",
        "btn_menu": "« Menu",
        "prompt_add": "Inviami il numero della pratica.\nEsempio: <code>26NA123456</code>",
        "prompt_remove": "Scegli una pratica da rimuovere:",
        "case_added": "✅ Pratica <code>{case}</code> aggiunta.\nStato attuale: {status}",
        "case_exists": "⚠️ La pratica <code>{case}</code> è già monitorata.",
        "case_not_found": "❌ Pratica <code>{case}</code> non trovata nell'archivio.",
        "case_removed": "✅ Pratica <code>{case}</code> rimossa dal monitoraggio.",
        "case_not_tracked": "⚠️ La pratica <code>{case}</code> non è nella tua lista.",
        "status_header": "📋 Le tue pratiche:\n",
        "status_row": "{i}. <code>{case}</code> — {status}\n   <i>(controllato: {checked})</i>",
        "no_cases": "Non hai pratiche monitorate.",
        "status_changed": "🔔 Lo stato della pratica <code>{case}</code> è cambiato!\n\nNuovo stato: {status}",
        "btn_check_website": "🌐 Controlla sul sito",
        "check_error": "⚠️ Impossibile controllare lo stato della pratica <code>{case}</code>.",
        "limit_reached": "⚠️ Limite raggiunto (10 pratiche). Rimuovine alcune prima.",
        "not_registered": "Per favore, inizia con /start per scegliere la lingua.",
        "checking": "⏳ Verifica della pratica <code>{case}</code>…",
    },
}


def t(lang: str, key: str, **kwargs) -> str:
    strings = STRINGS.get(lang, STRINGS["en"])
    template = strings.get(key, STRINGS["en"].get(key, key))
    return template.format(**kwargs) if kwargs else template
