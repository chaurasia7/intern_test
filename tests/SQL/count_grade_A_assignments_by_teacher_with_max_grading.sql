WITH TeacherAssignmentCounts AS (
    SELECT 
        teacher_id,
        COUNT(*) AS total_assignments
    FROM assignments
    WHERE state = 'GRADED'
    GROUP BY teacher_id
    ORDER BY total_assignments DESC, teacher_id ASC
    LIMIT 1
)
SELECT COUNT(*) AS grade_A_count
FROM assignments
WHERE state = 'GRADED' 
AND teacher_id = (SELECT teacher_id FROM TeacherAssignmentCounts)
AND grade = 'A';
