# fix-ingmobile-on-huawei

Klienci ING korzystający z telefonów Huawei zostali dzisiaj wylogowani, a próba zalogowania się do aplikacji kończy się komunikatem

> Aplikacja, z której korzystasz została pobrana z nieautoryzowanego przez nas źródła. Pobierz naszą aplikację z App Store lub Google Play.

Jak sobie poradzić?

1. Włącz tryb deweloperski na Androidzie ( https://developer.android.com/studio/debug/dev-options )
2. Zainstaluj `adb` (zawarte w https://developer.android.com/studio , sekcja "Command line tools only"). Sensowne dystrubycje linuksa posiadają również `adb` w repozytoriach.
3. Pobierz skrypt `fix_ing.py` z tego repozytorium.
4. Upewnij się, że aplikacja Moje ING jest zainstalowana.
5. Podłącz telefon do komputera kablem USB.
6. Uruchom skrypt: `python3 ./fix_ing.py`.

Skrypt był testowany na Linuksie (Fedora). Ma również spore szanse działać na macOS. Ma duże szanse **nie** działać na Windowsie.
