import os
from sqlalchemy import text
import random  # Add this import
from core import db
from core.models.assignments import Assignment, AssignmentStateEnum, GradeEnum


def create_n_graded_assignments_for_teacher(number: int = 0, teacher_id: int = 1) -> int:
    """
       Creates 'n' graded assignments for a specified teacher and returns the count of assignments with grade 'A'.

       Parameters:
       - number (int): The number of assignments to be created.
       - teacher_id (int): The ID of the teacher for whom the assignments are created.

       Returns:
       - int: Count of assignments with grade 'A'.
       """

    grade_a_counter: int = Assignment.filter(
        Assignment.teacher_id == teacher_id,
        Assignment.grade == GradeEnum.A
    ).count()

    for _ in range(number):
        grade = random.choice(list(GradeEnum))
        assignment = Assignment(
            teacher_id=teacher_id,
            student_id=1,
            grade=grade,
            content='test content',
            state=AssignmentStateEnum.GRADED
        )
        db.session.add(assignment)
        if grade == GradeEnum.A:
            grade_a_counter += 1

    db.session.commit()
    return grade_a_counter


def test_get_assignments_in_graded_state_for_each_student():
    """Test to get graded assignments for each student"""

    submitted_assignments = Assignment.filter(Assignment.student_id == 1)
    for assignment in submitted_assignments:
        assignment.state = AssignmentStateEnum.GRADED

    db.session.flush()
    db.session.commit()

    expected_result = [(1, 3)]

    sql_file_path = os.path.join(os.path.dirname(__file__), 'number_of_graded_assignments_for_each_student.sql')
    with open(sql_file_path, encoding='utf8') as fo:
        sql = fo.read()

    sql_result = db.session.execute(text(sql)).fetchall()
    print(f"Expected: {expected_result}, SQL Result: {sql_result}")
    for itr, result in enumerate(expected_result):
        assert result[0] == sql_result[itr][0]


def test_get_grade_A_assignments_for_teacher_with_max_grading():
    """Test to get count of grade A assignments for teacher which has graded maximum assignments"""

    sql_file_path = os.path.join(os.path.dirname(__file__), 'count_grade_A_assignments_by_teacher_with_max_grading.sql')
    with open(sql_file_path, encoding='utf8') as fo:
        sql = fo.read()

    # Test setup for teacher_id=1
    grade_a_count_1 = create_n_graded_assignments_for_teacher(5)
    sql_result = db.session.execute(text(sql)).fetchall()
    assert grade_a_count_1 == sql_result[0][0]

    # Test setup for teacher_id=2
    grade_a_count_2 = create_n_graded_assignments_for_teacher(10, 2)
    sql_result = db.session.execute(text(sql)).fetchall()

    # Check if the expected result is equal to the actual result
    assert grade_a_count_2 == sql_result[0][0]
