import time
import requests


class GetUrl:
    """Entering arguments in sequence: job, experience, placement period.
Jobs can be searched in languages supported by hh.ru. Recommendations: Russian or English.
Experience input: 0 - no experience, 1 - from 1 to 3 years, 2 - from 3 to 6 years, 3 - more than 6
Max period = 30, interval - [0; 30]\n"""

    URL = 'https://api.hh.ru/vacancies'

    dict_experience = {'0': 'noExperience', '1': 'between1And3', '2': 'between3And6', '3': 'moreThan6'}

    def __init__(self, job, experience, period):
        self.job = job
        self.experience = GetUrl.dict_experience[experience]
        self.period = period
        self.dict_get = {'text': f'NAME:{self.job}', 'period': self.period, 'per_page': 50,
                         'responses_count_enabled': True, 'experience': self.experience}

    def get_request(self):
        return requests.get(GetUrl.URL, params=self.dict_get)


class CreateListVacancies:
    """This is a functor. It generates a string with information about each vacancy when a class object is called."""

    def __init__(self):
        self.list_vacancies = []

    def __call__(self, dict_json, *args, **kwargs):
        for vacancy in dict_json['items']:
            self.list_vacancies.append(self.create_str_vacancy(vacancy))

    @staticmethod
    def create_str_vacancy(vacancy):
        return f' | {vacancy["name"]} | {vacancy["alternate_url"]} | Отклики: {vacancy["counters"]["responses"]} | Город: {vacancy["area"]["name"]} | Компания: {vacancy["employer"]["name"]}| Тип работы: {vacancy["schedule"]["name"]}'


class WriteToFile:

    """When the parser is launched, a file will be created with the name that you pass as an argument when creating a class object"""

    DATE_TODAY = time.strftime('%d|%B|%Y-%H:%M:%S')

    def __init__(self, file_name=f'{DATE_TODAY}-report'):
        self.file_name = f'{file_name}'

    def write(self, vacancies):
        with open(self.file_name, 'w+') as information_file:
            for vacancy in vacancies:
                information_file.write(f'{vacancy}\n')
        print(f'Your file is done! Name file: {self.file_name}')


def main():
    print(GetUrl.__doc__)
    url_job = GetUrl(input('Your job: '), input('Your experience: '), input('Period: '))
    validator = CreateListVacancies()  # create functor
    validator(url_job.get_request().json())
    list_vacancies = validator.list_vacancies
    writer = WriteToFile()
    writer.write(list_vacancies)


if __name__ == '__main__':
    main()
