

import logging
from django.http import HttpResponse
from django.shortcuts import render
from django.db import connection

# Получаем логгеры
logger = logging.getLogger('django')
security_logger = logging.getLogger('django.security')


def test_logging(request):
    """
    Тестирование всех уровней логирования
    """
    # Разные уровни сообщений
    logger.debug("🐞 DEBUG сообщение для консоли")
    logger.info("ℹ️ INFO сообщение")
    logger.warning("⚠️ WARNING сообщение с pathname")

    # Тестируем ошибку со стеком
    try:
        result = 10 / 0
    except ZeroDivisionError as e:
        logger.error("❌ Ошибка деления на ноль!", exc_info=True)
        logger.critical("🔥 Критическая ошибка в системе!", exc_info=True)

    # Тестируем security логи
    security_logger.info("🔒 Попытка несанкционированного доступа к админке")
    security_logger.warning("⚠️ Обнаружена подозрительная активность")

    return HttpResponse("✅ Логирование протестировано! Проверьте консоль и файлы логов.")


def test_template_error(request):
    """
    Тест ошибки в шаблоне
    """
    context = {'value': None}
    return render(request, 'myapp/test.html', context)


def test_db_error(request):
    """
    Тест ошибки базы данных
    """
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM non_existent_table")
    except Exception as e:
        logger.error("💾 Ошибка базы данных!", exc_info=True)
        return HttpResponse(f"❌ Ошибка БД: {str(e)}")

    return HttpResponse("✅ OK")