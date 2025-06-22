from dto.g1_scraper import G1Scraper
from dto.exame_scraper import ExameScraper
from dto.carta_scraper import CartaCapitalScraper
from dto.moneytimes_scraper import MoneyTimesScraper
from dto.suno_scraper import SunoScraper
from service.run_scrapers import run_scraper_db

class UserInput:
    def user_input():
        print("\nBem-vindo ao Keyword Monitor!\nEssa ferramenta coleta notícias de portais brasileiros e conta a quantidade de ocorrências de uma palavra-chave no corpo de cada artigo.")
        while True:
            portal = input("\nVocê deseja analisar qual desses portais?\n1 - G1\n2 - Exame\n3 - Carta Capital\n4 - Money Times\n5 - Suno\n6 - Todos\n7 - Sair\n")
            match portal:
                case "1":
                    g1_scraper = G1Scraper()
                    portal_name = "g1"
                    periodo = input("\nVocê deseja analisar qual período?\n1 - 1 hora\n2 - Hoje \n3 - 7 dias\n")
                    match periodo:
                        case "1":
                            run_scraper_db(g1_scraper, ['minuto', 'minutos'], portal_name)
                        case "2":
                            run_scraper_db(g1_scraper, ['minuto', 'minutos', 'hora', 'horas'], portal_name)
                        case "3":
                            run_scraper_db(g1_scraper, ['minuto', 'minutos', 'hora', 'horas', "ontem", 'dia', 'dias'], portal_name)
                        case _:
                            print("\n===========\nOpção inválida. Tente novamente.\n===========\n")
                            continue
                case "2":
                    exame_scraper = ExameScraper()
                    portal_name = "exame"
                    periodo = input("\nVocê deseja analisar qual período?\n1 - 1 hora\n2 - Hoje\n3 - 7 dias\n4 - 30 dias\n")
                    match periodo:
                        case "1":
                            run_scraper_db(exame_scraper, 1, portal_name)
                        case "2":
                            run_scraper_db(exame_scraper, 2, portal_name)
                        case "3":
                            run_scraper_db(exame_scraper, 3, portal_name)
                        case "4":
                            run_scraper_db(exame_scraper, 4, portal_name)
                        case _:
                            print("\n===========\nOpção inválida. Tente novamente.\n===========\n")
                            continue
                case "3":
                    carta_scraper = CartaCapitalScraper()
                    portal_name = "carta_capital"
                    periodo = input("\nVocê deseja analisar qual período?\n1 - 1 hora\n2 - Hoje\n3 - 7 dias\n4 - 30 dias\n")
                    match periodo:
                        case "1":
                            run_scraper_db(carta_scraper, 1, portal_name)
                        case "2":
                            run_scraper_db(carta_scraper, 2, portal_name)
                        case "3":
                            run_scraper_db(carta_scraper, 3, portal_name)
                        case "4":
                            run_scraper_db(carta_scraper, 4, portal_name)
                        case _:
                            print("\n===========\nOpção inválida. Tente novamente.\n===========\n")
                            continue
                case "4":
                    moneytimes_scraper = MoneyTimesScraper()
                    portal_name = "moneytimes"
                    periodo = input("\nVocê deseja analisar qual período?\n1 - 1 hora\n2 - Hoje\n3 - 30 dias\n")
                    match periodo:
                        case "1":
                            run_scraper_db(moneytimes_scraper,['minuto', 'minutos'], portal_name)
                        case "2":
                            run_scraper_db(moneytimes_scraper, ['minuto', 'minutos', 'hora', 'horas'], portal_name)
                        case "3":
                            run_scraper_db(moneytimes_scraper, ['minuto', 'minutos', 'hora', 'horas', "ontem", 'dia', 'dias', 'mes', 'meses'], portal_name)
                        case _:
                            print("\n===========\nOpção inválida. Tente novamente.\n===========\n")
                            continue
                case "5":
                    suno_scraper = SunoScraper()
                    portal_name = "suno"
                    periodo = input("\nVocê deseja analisar qual período?\n1 - 1 hora\n2 - Hoje\n3 - 7 dias\n4 - 30 dias\n")
                    match periodo:
                        case "1":
                            run_scraper_db(suno_scraper, 1, portal_name)
                        case "2":
                            run_scraper_db(suno_scraper, 2, portal_name)
                        case "3":
                            run_scraper_db(suno_scraper, 3, portal_name)
                        case "4":
                            run_scraper_db(suno_scraper, 4, portal_name)
                        case _:
                            print("\n===========\nOpção inválida. Tente novamente.\n===========\n")
                            continue
                case "6":
                        print("\n===========\nOpção em produção.\n===========\n")
                        continue
                case "7":
                    break
                case _:
                    print("\n===========\nOpção inválida. Tente novamente.\n===========\n")
                    continue
                
                    