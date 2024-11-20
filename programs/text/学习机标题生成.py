import random

def xuexiji_name():
    first_name = [
        '科大讯飞同款学习机',
        '科大讯飞T30同款学习机',
        '科大讯飞T30pro同款学习机',
        '科大讯飞同款AI智能学习机',
    ]

    second_name = [
        '智能学习平板电脑',
    ]

    third_name = [
        '护眼学习机',
        '高清护眼学习机',
        'AI护眼学习机',
    ]

    forth_name = [
        '步步高同款学习机',
        '步步高S8同款学习机',
    ]

    fifth_name = [
        '小学初中高中同步更新',
    ]

    xuexiji_name = random.choice(first_name) + random.choice(second_name) + random.choice(third_name) + random.choice(forth_name) + random.choice(fifth_name)

    return xuexiji_name