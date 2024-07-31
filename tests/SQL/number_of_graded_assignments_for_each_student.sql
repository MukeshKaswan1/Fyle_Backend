-- Write query to get number of graded assignments for each student:

SELECT student_id, COUNT(*) AS no_of_graded_assignment
FROM assignments
WHERE grade IS NOT NULL
GROUP BY student_id;
