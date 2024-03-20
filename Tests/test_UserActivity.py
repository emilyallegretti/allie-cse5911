import pandas as pd
from EventContainers import UserActivity  

def test_calculate_time_spent_per_day_single_user():
    data = {
        'user_id': [1, 1],
        'timestamp': ['2024-03-19 08:00:00', '2024-03-19 10:00:00'],
        'page': ['LoginPage', 'HomePage'],
    }
    activities = pd.DataFrame(data)
    activities['timestamp'] = pd.to_datetime(activities['timestamp'])
    
    result = UserActivity.calculate_time_spent_per_day(activities)
    
    expected_time_spent = "2h 0m"
    assert result.iloc[0]['total_time_spent'] == expected_time_spent


def test_count_login_page_activities_per_day():
    data = {
        'user_id': [1, 1, 2, 2],
        'timestamp': [
            '2024-03-19 08:00:00',
            '2024-03-19 09:00:00',
            '2024-03-19 10:00:00',
            '2024-03-20 11:00:00'
        ],
        'activityType': ['Login Page', 'Home Page', 'Login Page', 'Login Page'],
    }
    activities = pd.DataFrame(data)
    activities['timestamp'] = pd.to_datetime(activities['timestamp'])

    result_all_users = UserActivity.count_login_page_activities_per_day(activities)
    assert len(result_all_users) == 3  
    assert all(result_all_users['login_count'] == 1)  
    user_id = 1
    result_specific_user = UserActivity.count_login_page_activities_per_day(activities, user_id=user_id)
    assert len(result_specific_user) == 1  
    assert result_specific_user.iloc[0]['login_count'] == 1
    assert result_specific_user.iloc[0]['user_id'] == user_id
