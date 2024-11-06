Application Logs
2024-11-06T12:45:14.309752+00:00 app[worker.1]: sys:1: RuntimeWarning: coroutine 'Application.initialize' was never awaited
2024-11-06T12:45:14.309753+00:00 app[worker.1]: Object allocated at (most recent call last):
2024-11-06T12:45:14.309754+00:00 app[worker.1]:   File "/app/.heroku/python/lib/python3.10/site-packages/telegram/ext/_application.py", lineno 1079
2024-11-06T12:45:14.309754+00:00 app[worker.1]:     loop.run_until_complete(self.initialize())
2024-11-06T12:45:14.309868+00:00 app[worker.1]: sys:1: RuntimeWarning: coroutine 'Application.stop' was never awaited
2024-11-06T12:45:14.309869+00:00 app[worker.1]: Object allocated at (most recent call last):
2024-11-06T12:45:14.309870+00:00 app[worker.1]:   File "/app/.heroku/python/lib/python3.10/site-packages/telegram/ext/_application.py", lineno 1100
2024-11-06T12:45:14.309870+00:00 app[worker.1]:     loop.run_until_complete(self.stop())
2024-11-06T12:45:14.418656+00:00 heroku[worker.1]: Process exited with status 0
2024-11-06T12:45:14.441676+00:00 heroku[worker.1]: State changed from up to crashed
2024-11-06T12:46:00.871435+00:00 heroku[worker.1]: State changed from crashed to starting
2024-11-06T12:46:02.199130+00:00 heroku[worker.1]: Starting process with command `python main.py`
2024-11-06T12:46:02.844325+00:00 heroku[worker.1]: State changed from starting to up
2024-11-06T12:46:03.740024+00:00 app[worker.1]: INFO:__main__:🔄 Бот запущено.
2024-11-06T12:46:03.888263+00:00 app[worker.1]: INFO:httpx:HTTP Request: POST https://api.telegram.org/bot7721474356:AAEYb4YIEAKCCxMl3uxT8t__KAiwQ4UopkQ/getMe "HTTP/1.1 200 OK"
2024-11-06T12:46:03.890048+00:00 app[worker.1]: INFO:telegram.ext.Application:Application started
2024-11-06T12:46:03.891606+00:00 app[worker.1]: INFO:telegram.ext.Application:Application is stopping. This might take a moment.
2024-11-06T12:46:03.891837+00:00 app[worker.1]: INFO:telegram.ext.Application:Application.stop() complete
2024-11-06T12:46:03.895673+00:00 app[worker.1]: ERROR:__main__:Помилка при виконанні: Cannot close a running event loop
2024-11-06T12:46:03.911183+00:00 app[worker.1]: sys:1: RuntimeWarning: coroutine 'Application.initialize' was never awaited
2024-11-06T12:46:03.911184+00:00 app[worker.1]: Object allocated at (most recent call last):
2024-11-06T12:46:03.911185+00:00 app[worker.1]:   File "/app/.heroku/python/lib/python3.10/site-packages/telegram/ext/_application.py", lineno 1079
2024-11-06T12:46:03.911185+00:00 app[worker.1]:     loop.run_until_complete(self.initialize())
2024-11-06T12:46:03.911296+00:00 app[worker.1]: sys:1: RuntimeWarning: coroutine 'Application.stop' was never awaited
2024-11-06T12:46:03.911296+00:00 app[worker.1]: Object allocated at (most recent call last):
2024-11-06T12:46:03.911296+00:00 app[worker.1]:   File "/app/.heroku/python/lib/python3.10/site-packages/telegram/ext/_application.py", lineno 1100
2024-11-06T12:46:03.911296+00:00 app[worker.1]:     loop.run_until_complete(self.stop())
2024-11-06T12:46:04.024945+00:00 heroku[worker.1]: Process exited with status 0
2024-11-06T12:46:04.048023+00:00 heroku[worker.1]: State changed from up to crashed