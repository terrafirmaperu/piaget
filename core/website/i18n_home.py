"""Textos de la portada en español, inglés y quechua."""

HOME_LANGS = (
    ('es', 'Español'),
    ('en', 'English'),
    ('qu', 'Runasimi'),
)

HOME_TEXTS = {
    'es': {
        'cta': 'Sin limites',
        'have_account': '¿Ya tienes cuenta?',
        'yes': 'Sí',
        'no': 'No',
        'hint_yes': 'Sí → usuario y contraseña',
        'hint_no': 'No → formulario de inscripción',
        'hint_demo': 'Demo → probar como invitado',
        'lang_label': 'Idioma',
        'page_title': 'Inicio · jean piaget IA',
        'welcome': 'Bienvenida',
        'welcome_to': 'a',
        'welcome_continue': 'Continuar',
        'account_title': 'Elige una opción',
        'have_account_btn': 'Tengo cuenta',
        'demo_btn': 'Demo',
        'demo_page_title': 'Demo · ¿Qué aprenderemos hoy?',
        'demo_heading': '¿Qué aprenderemos hoy, invitado?',
        'demo_sub': 'Elige una opción para empezar',
        'demo_back': 'Volver al inicio',
        'demo_back_options': 'Volver a las opciones',
        'demo_coming': 'Pronto podrás practicar aquí. Esta es la demo de invitado.',
        'opt_matematicas': 'Matemáticas',
        'opt_lenguaje': 'Lenguaje',
        'opt_arte': 'Arte',
        'opt_ciencias': 'Ciencias',
        'opt_historia': 'Historia',
        'opt_tecnologia': 'Tecnología',
    },
    'en': {
        'cta': 'Without limits',
        'have_account': 'Do you already have an account?',
        'yes': 'Yes',
        'no': 'No',
        'hint_yes': 'Yes → username and password',
        'hint_no': 'No → registration form',
        'hint_demo': 'Demo → try as guest',
        'lang_label': 'Language',
        'page_title': 'Home · jean piaget IA',
        'welcome': 'Welcome',
        'welcome_to': 'to',
        'welcome_continue': 'Continue',
        'account_title': 'Choose an option',
        'have_account_btn': 'I have an account',
        'demo_btn': 'Demo',
        'demo_page_title': 'Demo · What will we learn today?',
        'demo_heading': 'What will we learn today, guest?',
        'demo_sub': 'Pick an option to start',
        'demo_back': 'Back to home',
        'demo_back_options': 'Back to options',
        'demo_coming': 'You will be able to practice here soon. This is the guest demo.',
        'opt_matematicas': 'Math',
        'opt_lenguaje': 'Language',
        'opt_arte': 'Art',
        'opt_ciencias': 'Science',
        'opt_historia': 'History',
        'opt_tecnologia': 'Technology',
    },
    'qu': {
        'cta': 'Mana saywakuna',
        'have_account': '¿Kayñachu yupayniyki kan?',
        'yes': 'Arí',
        'no': 'Mana',
        'hint_yes': 'Arí → ruraqpa sutin wan yaykuna rimay',
        'hint_no': 'Mana → qillqanakuy',
        'hint_demo': 'Demo → invitadu hina llamiy',
        'lang_label': 'Simi',
        'page_title': 'Qallariy · jean piaget IA',
        'welcome': 'Allillanchu',
        'welcome_to': '',
        'welcome_continue': 'Qatiy',
        'account_title': 'Akllay hukta',
        'have_account_btn': 'Yupayniy kan',
        'demo_btn': 'Demo',
        'demo_page_title': 'Demo · Ima yachasunchik?',
        'demo_heading': 'Ima yachasunchik kunan, invitadu?',
        'demo_sub': 'Akllay hukta qallarinanpaq',
        'demo_back': 'Wasiman kutiy',
        'demo_back_options': 'Akllaykunaman kutiy',
        'demo_coming': 'Pisi pachallapi kaypi ruwanayki kanqa. Kayqa demo invitadu.',
        'opt_matematicas': 'Yupay yachay',
        'opt_lenguaje': 'Simi',
        'opt_arte': 'Taki / llimphi',
        'opt_ciencias': 'Yachaykuna',
        'opt_historia': 'Ñawpa willakuy',
        'opt_tecnologia': 'Tecnología',
    },
}

DEMO_OPTION_SLUGS = (
    'matematicas',
    'lenguaje',
    'arte',
    'ciencias',
    'historia',
    'tecnologia',
)


def get_demo_options(code):
    t = get_home_texts(code)
    return [
        {'slug': 'matematicas', 'label': t['opt_matematicas']},
        {'slug': 'lenguaje', 'label': t['opt_lenguaje']},
        {'slug': 'arte', 'label': t['opt_arte']},
        {'slug': 'ciencias', 'label': t['opt_ciencias']},
        {'slug': 'historia', 'label': t['opt_historia']},
        {'slug': 'tecnologia', 'label': t['opt_tecnologia']},
    ]

DEFAULT_HOME_LANG = 'es'


def normalize_home_lang(code):
    code = (code or '').strip().lower()
    if code in HOME_TEXTS:
        return code
    return DEFAULT_HOME_LANG


def get_home_texts(code):
    return HOME_TEXTS[normalize_home_lang(code)]
