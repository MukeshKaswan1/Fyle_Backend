from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.teachers import Teacher
from core.models.assignments import Assignment

from .schema import TeacherSchema, AssignmentSchema, AssignmentGradeSchema

principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)


@principal_assignments_resources.route('/teachers', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_teachers(p):
    """Returns list of all teachers"""
    all_teachers = Teacher.get_all_teachers()
    all_teachers_dump = TeacherSchema().dump(all_teachers, many=True)
    return APIResponse.respond(data=all_teachers_dump)


@principal_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of submitted and graded assignments"""
    assignments = Assignment.get_submitted_and_graded_assignments()
    assignments_dump = AssignmentSchema().dump(assignments, many=True)
    return APIResponse.respond(data=assignments_dump)


@principal_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def regrade_assignment(p, incoming_payload):
    """Re-grade an assignment already graded by a teacher"""
    regrade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)
    print(p)

    try:
        regraded_assignment = Assignment.mark_grade(
            _id=regrade_assignment_payload.id,
            grade=regrade_assignment_payload.grade,
            auth_principal=p)
    except ValueError as e:
        return APIResponse.respond(error=str(e), status=400)

    regraded_assignment_dump = AssignmentSchema().dump(regraded_assignment)
    return APIResponse.respond(data=regraded_assignment_dump)




