from core.models.assignments import AssignmentStateEnum, GradeEnum


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
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 458,
            'grade': GradeEnum.A.value
        },
        headers=h_principal
    )

    assert response.status_code == 400


def test_grade_assignment(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
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
        json={
            'id': 3,
            'grade': GradeEnum.B.value
        },
        headers=h_principal
    )

    assert response.status_code == 200

    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.B


def test_regrade_assignment_invalid(client, h_principal):
    """Test to re-grade an assignment with invalid data"""
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 999,  # Assuming this ID does not exist
            'grade': GradeEnum.B.value
        },
        headers=h_principal
    )

    assert response.status_code == 404


def test_grade_assignment_empty_grade(client, h_principal):
    """
    failure case: If the grade is empty, it should return a 400 Bad Request status.
    """
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 6,  # Use an existing assignment ID
            'grade': ''  # Empty grade
        },
        headers=h_principal
    )

    assert response.status_code == 400


def test_get_teachers(client, h_principal):
    """Test to get the list of all teachers"""
    response = client.get('/principal/teachers', headers=h_principal)

    assert response.status_code == 200
    assert isinstance(response.json['data'], list)
    assert all('id' in teacher for teacher in response.json['data'])
    # assert all('student_id' in teacher for teacher in response.json['data'])
    assert all('created_at' in teacher for teacher in response.json['data'])
    assert all('updated_at' in teacher for teacher in response.json['data'])
