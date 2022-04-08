languagePoll = {
    'Bash': 0,
    'Python': 0,
    'PowerShell': 0,
}

while True:
    language = input("What is your favourite scripting language? Type q when done.")
    if language == 'q':
        break
    else:
        if language in languagePoll.keys():
            languagePoll[language] += 1

print(languagePoll)