from flask import Blueprint
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment,AssignmentStateEnum
from core import db
from .schema import AssignmentSchema, AssignmentGradeSchema
from core.libs import assertions

teacher_assignments_resources = Blueprint('teacher_assignments_resources', __name__)


@teacher_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of assignments"""
    teachers_assignments = Assignment.get_assignments_by_teacher(p.teacher_id)
    teachers_assignments_dump = AssignmentSchema().dump(teachers_assignments, many=True)
    return APIResponse.respond(data=teachers_assignments_dump)



@teacher_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p, incoming_payload):
    submit_assignment_payload = AssignmentGradeSchema().load(incoming_payload)

    # Fetch the assignment by its ID
    graded_assignment = Assignment.get_by_id(submit_assignment_payload.id)
    
    if not graded_assignment:
        assertions.base_assert(404,"Assignment does not exist")

    if graded_assignment.teacher_id != p.teacher_id:
        assertions.base_assert(400,"Submission to Wrong teacher")

    # Grade the assignment
        graded_assignment = Assignment.mark_grade(
            _id=submit_assignment_payload.id,
            grade=submit_assignment_payload.grade,
            auth_principal=p
        )

        db.session.commit()

        grade_assignment_dump = AssignmentSchema().dump(graded_assignment)
        return APIResponse.respond(data=grade_assignment_dump)
