def sort_the_dictionary(company_profit_percentage):
    sorted_company_profit_percentage = sorted(company_profit_percentage.items(), key=lambda item: item[1],reverse=True)
    return sorted_company_profit_percentage