/*
 * Example Java Program - Student Management System
 * Demonstrates various Java constructs for Halstead Metrics analysis
 */

import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class StudentManagement {
    
    private List<Student> students;
    private Scanner scanner;
    
    public StudentManagement() {
        this.students = new ArrayList<>();
        this.scanner = new Scanner(System.in);
    }
    
    // Inner class for Student
    static class Student {
        private String name;
        private int id;
        private double[] grades;
        private double average;
        
        public Student(String name, int id, double[] grades) {
            this.name = name;
            this.id = id;
            this.grades = grades;
            this.average = calculateAverage(grades);
        }
        
        private double calculateAverage(double[] grades) {
            if (grades == null || grades.length == 0) {
                return 0.0;
            }
            
            double sum = 0.0;
            for (double grade : grades) {
                sum += grade;
            }
            return sum / grades.length;
        }
        
        public String getName() {
            return name;
        }
        
        public int getId() {
            return id;
        }
        
        public double getAverage() {
            return average;
        }
        
        public String getGrade() {
            if (average >= 90) return "A";
            else if (average >= 80) return "B";
            else if (average >= 70) return "C";
            else if (average >= 60) return "D";
            else return "F";
        }
    }
    
    // Add a new student
    public void addStudent() {
        System.out.print("Enter student name: ");
        String name = scanner.nextLine();
        
        System.out.print("Enter student ID: ");
        int id = Integer.parseInt(scanner.nextLine());
        
        System.out.print("Enter number of grades: ");
        int numGrades = Integer.parseInt(scanner.nextLine());
        double[] grades = new double[numGrades];
        
        for (int i = 0; i < numGrades; i++) {
            System.out.print("Enter grade " + (i + 1) + ": ");
            grades[i] = Double.parseDouble(scanner.nextLine());
        }
        
        Student student = new Student(name, id, grades);
        students.add(student);
        System.out.println("Student added successfully!");
    }
    
    // Find student by ID
    public Student findStudentById(int id) {
        for (Student student : students) {
            if (student.getId() == id) {
                return student;
            }
        }
        return null;
    }
    
    // Calculate class statistics
    public void displayStatistics() {
        if (students.isEmpty()) {
            System.out.println("No students in the system.");
            return;
        }
        
        double totalAverage = 0.0;
        double maxAverage = Double.MIN_VALUE;
        double minAverage = Double.MAX_VALUE;
        int aCount = 0, bCount = 0, cCount = 0, dCount = 0, fCount = 0;
        
        for (Student student : students) {
            double avg = student.getAverage();
            totalAverage += avg;
            
            if (avg > maxAverage) {
                maxAverage = avg;
            }
            if (avg < minAverage) {
                minAverage = avg;
            }
            
            String grade = student.getGrade();
            switch (grade) {
                case "A":
                    aCount++;
                    break;
                case "B":
                    bCount++;
                    break;
                case "C":
                    cCount++;
                    break;
                case "D":
                    dCount++;
                    break;
                case "F":
                    fCount++;
                    break;
            }
        }
        
        double classAverage = totalAverage / students.size();
        
        System.out.println("\n=== Class Statistics ===");
        System.out.println("Total Students: " + students.size());
        System.out.println("Class Average: " + String.format("%.2f", classAverage));
        System.out.println("Highest Average: " + String.format("%.2f", maxAverage));
        System.out.println("Lowest Average: " + String.format("%.2f", minAverage));
        System.out.println("\nGrade Distribution:");
        System.out.println("A: " + aCount + " | B: " + bCount + " | C: " + cCount + 
                         " | D: " + dCount + " | F: " + fCount);
    }
    
    // Display all students
    public void displayAllStudents() {
        if (students.isEmpty()) {
            System.out.println("No students in the system.");
            return;
        }
        
        System.out.println("\n=== All Students ===");
        for (Student student : students) {
            System.out.println("ID: " + student.getId() + 
                             " | Name: " + student.getName() + 
                             " | Average: " + String.format("%.2f", student.getAverage()) +
                             " | Grade: " + student.getGrade());
        }
    }
    
    // Main menu
    public void showMenu() {
        System.out.println("\n=== Student Management System ===");
        System.out.println("1. Add Student");
        System.out.println("2. Find Student by ID");
        System.out.println("3. Display All Students");
        System.out.println("4. Display Statistics");
        System.out.println("5. Exit");
        System.out.print("Enter your choice: ");
    }
    
    // Main method
    public static void main(String[] args) {
        StudentManagement system = new StudentManagement();
        Scanner scanner = new Scanner(System.in);
        boolean running = true;
        
        while (running) {
            system.showMenu();
            int choice = Integer.parseInt(scanner.nextLine());
            
            switch (choice) {
                case 1:
                    system.addStudent();
                    break;
                case 2:
                    System.out.print("Enter student ID: ");
                    int id = Integer.parseInt(scanner.nextLine());
                    Student found = system.findStudentById(id);
                    if (found != null) {
                        System.out.println("Found: " + found.getName() + 
                                         " | Average: " + String.format("%.2f", found.getAverage()) +
                                         " | Grade: " + found.getGrade());
                    } else {
                        System.out.println("Student not found!");
                    }
                    break;
                case 3:
                    system.displayAllStudents();
                    break;
                case 4:
                    system.displayStatistics();
                    break;
                case 5:
                    running = false;
                    System.out.println("Exiting...");
                    break;
                default:
                    System.out.println("Invalid choice!");
            }
        }
        
        scanner.close();
    }
}

