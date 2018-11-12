# config: utf-8

    # data type:
    # 1. discrete data sort by ratio (textual)
    # 2. discrete data sort by key (numerical)
    # 3. contious data sort by key, plot scater

    # 1 work class
    # 3 education
    # 5 martial status
    # 6 occupation
    # 7 relationship
    # 8 race
    # 9 sex
    # 13 native country

    # 0 age
    # 4 education number
    # 12 hours.per.week

    # 10 capital gain
    # 2 fnlwgt
    # 11 capatal loss

if __name__ == '__main__':
    from basic import get_raw_data_package
    print get_quantized_data()
