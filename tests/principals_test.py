from core.models.assignments import AssignmentStateEnum, GradeEnum
# ////////////////////////////////////////////////////////////
# Adding test case to call the landing page to check ./ working
import pytest
from core import app

@pytest.fixture
def client():
    """Test client for the Flask application"""
    with app.test_client() as client:
        yield client

def test_to_check_initial_route(client):
    """Test the `/` route for the health check"""
    response = client.get('/')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['status'] == 'ready'
    assert 'time' in json_data
# /////////////////////////////////////////////////////////////



def test_get_assignments(client, h_principal):
    response = client.get(
        '/principal/assignments',
        headers=h_principal
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['state'] in [AssignmentStateEnum.SUBMITTED, AssignmentStateEnum.GRADED]


def test_grade_assignment_draft_assignment(client, h_principal):
    """
    failure case: If an assignment is in Draft state, it cannot be graded by principal
    """
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 5,
            'grade': GradeEnum.A.value
        },
        headers=h_principal
    )

    assert response.status_code == 400


def test_grade_assignment(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        #This test case is supposed to grade an assignment and only submitted assignment can be graded
        #Default id=4 assignemnt is not submitted in my db so i had to give id of submiited assignment
        json={
            'id': 2,
            'grade': GradeEnum.C.value
        },
        headers=h_principal
    )

    assert response.status_code == 200

    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.C


def test_regrade_assignment(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        #This test case is supposed to regrade an assignment and only submitted assignment can be graded
        #Default id=4 assignemnt is not submitted in my db so i had to give id of submiited assignment
        json={
            'id': 2,
            'grade': GradeEnum.B.value
        },
        headers=h_principal
    )

    assert response.status_code == 200

    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.B
