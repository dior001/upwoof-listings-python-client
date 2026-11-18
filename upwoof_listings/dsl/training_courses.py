from typing import Any, Dict, List, Optional
from .. import resources

class TrainingCoursesDSL:
    def get_training_courses(self, params: Optional[Dict[str, Any]] = None) -> List[resources.TrainingCourse]:
        """The caller's listings' group training courses, by title (without `places_left`). Optional
        `active`, `listing_id`, `page`, `per_page` in `params`."""
        return resources.TrainingCourse.parse(self.request('get', 'training_courses', query=params))

    def get_training_course(self, *, resource_id: str) -> resources.TrainingCourse:
        """One course, including `places_left`."""
        if not resource_id:
            raise ValueError("ID cannot be blank")
        return resources.TrainingCourse.parse(self.request('get', f"training_courses/{resource_id}"))

    def get_training_course_sessions(self, *, training_course_id: str, params: Optional[Dict[str, Any]] = None
                                     ) -> List[resources.TrainingClassSession]:
        """Earliest first; `upcoming=True` lists only sessions that haven't ended."""
        if not training_course_id:
            raise ValueError("ID cannot be blank")
        path = f"training_courses/{training_course_id}/sessions"
        return resources.TrainingClassSession.parse(self.request('get', path, query=params))

    def get_training_course_enrollments(self, *, training_course_id: str, params: Optional[Dict[str, Any]] = None
                                        ) -> List[resources.TrainingEnrollment]:
        """Oldest first; optional `status` (enrolled, completed, cancelled)."""
        if not training_course_id:
            raise ValueError("ID cannot be blank")
        path = f"training_courses/{training_course_id}/enrollments"
        return resources.TrainingEnrollment.parse(self.request('get', path, query=params))

    def create_training_course_enrollment(self, *, training_course_id: str,
                                          params: Dict[str, Any]) -> resources.TrainingEnrollment:
        """Enroll `pet_id` (an active pet of a customer of the course's listing or its group). Optional
        `reservation_id` (one of that pet's stays there, which completing the course bills onto) and
        `use_membership_credit`. Raises ClientError (HTTP 403) for a course off sale, ResourceNotFoundError
        for an unknown course or pet, and ValidationError (HTTP 422) when the course is full, the pet is
        already enrolled, the stay isn't the pet's there, a payment is in progress online, or no training
        membership credit is left."""
        if not training_course_id:
            raise ValueError("ID cannot be blank")
        path = f"training_courses/{training_course_id}/enrollments"
        return resources.TrainingEnrollment.parse(self.request('post', path, query=params))

    def get_training_course_waitlist_entries(self, *, training_course_id: str,
                                             params: Optional[Dict[str, Any]] = None
                                             ) -> List[resources.TrainingWaitlistEntry]:
        """In line order; optional `status` (waiting, offered, enrolled, removed)."""
        if not training_course_id:
            raise ValueError("ID cannot be blank")
        path = f"training_courses/{training_course_id}/waitlist_entries"
        return resources.TrainingWaitlistEntry.parse(self.request('get', path, query=params))

    def get_training_enrollment(self, *, resource_id: str) -> resources.TrainingEnrollment:
        if not resource_id:
            raise ValueError("ID cannot be blank")
        return resources.TrainingEnrollment.parse(self.request('get', f"training_enrollments/{resource_id}"))

    def cancel_training_enrollment(self, *, resource_id: str) -> resources.TrainingEnrollment:
        """Raises ValidationError (HTTP 422) when the enrollment is already completed or cancelled."""
        if not resource_id:
            raise ValueError("ID cannot be blank")
        path = f"training_enrollments/{resource_id}/cancel"
        return resources.TrainingEnrollment.parse(self.request('post', path))
