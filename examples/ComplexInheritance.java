/*
 * Complex Inheritance Example - Demonstrates Deep Inheritance and Multiple Children
 * This example creates a deep inheritance hierarchy to test DIT and NOC metrics
 */

import java.util.*;
import java.io.*;

// Root class (DIT = 0)
abstract class Animal {
    protected String name;
    protected int age;
    
    public Animal(String name, int age) {
        this.name = name;
        this.age = age;
    }
    
    // Abstract method
    public abstract void makeSound();
    
    // Method with if (CC = 2)
    public boolean isAdult() {
        if (age >= 1) {
            return true;
        }
        return false;
    }
    
    // Method with switch (CC = 1 + cases)
    public String getCategory() {
        switch (age) {
            case 0:
                return "Baby";
            case 1:
            case 2:
                return "Young";
            default:
                return "Adult";
        }
    }
}

// Level 1 (DIT = 1)
class Mammal extends Animal {
    private boolean hasFur;
    
    public Mammal(String name, int age, boolean hasFur) {
        super(name, age);
        this.hasFur = hasFur;
    }
    
    @Override
    public void makeSound() {
        System.out.println(name + " makes a mammal sound");
    }
    
    // Method with while and if (CC = 3)
    public void feed(int times) {
        int count = 0;
        while (count < times) {
            if (count % 2 == 0) {
                System.out.println("Feeding " + name);
            }
            count++;
        }
    }
}

// Level 2 (DIT = 2)
class Dog extends Mammal {
    private String breed;
    private List<String> tricks;
    
    public Dog(String name, int age, String breed) {
        super(name, age, true);
        this.breed = breed;
        this.tricks = new ArrayList<>();
    }
    
    @Override
    public void makeSound() {
        System.out.println(name + " barks: Woof!");
    }
    
    // Complex method (CC = 5: base + for + if + && + ||)
    public void performTricks() {
        for (String trick : tricks) {
            if (trick != null && (trick.equals("sit") || trick.equals("roll"))) {
                System.out.println(name + " performs: " + trick);
            }
        }
    }
    
    // Method with try-catch and if (CC = 3)
    public void learnTrick(String trick) {
        try {
            if (trick != null && !tricks.contains(trick)) {
                tricks.add(trick);
            }
        } catch (Exception e) {
            System.out.println("Error learning trick");
        }
    }
}

// Level 3 (DIT = 3)
class Puppy extends Dog {
    private boolean isHouseTrained;
    
    public Puppy(String name, int age, String breed) {
        super(name, age, breed);
        this.isHouseTrained = false;
    }
    
    @Override
    public void makeSound() {
        System.out.println(name + " yelps: Yip yip!");
    }
    
    // Method with do-while and if-else (CC = 4)
    public void train() {
        int attempts = 0;
        do {
            attempts++;
            if (attempts > 5) {
                isHouseTrained = true;
            } else {
                System.out.println("Training attempt " + attempts);
            }
        } while (!isHouseTrained && attempts < 10);
    }
}

// Another Level 2 (DIT = 2) - sibling of Dog
class Cat extends Mammal {
    private boolean isIndoor;
    
    public Cat(String name, int age, boolean isIndoor) {
        super(name, age, true);
        this.isIndoor = isIndoor;
    }
    
    @Override
    public void makeSound() {
        System.out.println(name + " meows: Meow!");
    }
    
    // Method with for and nested if (CC = 3)
    public void hunt(int hours) {
        for (int i = 0; i < hours; i++) {
            if (i % 2 == 0) {
                if (isIndoor) {
                    System.out.println(name + " plays indoors");
                }
            }
        }
    }
}

// Another Level 1 (DIT = 1) - sibling of Mammal
class Bird extends Animal {
    private boolean canFly;
    
    public Bird(String name, int age, boolean canFly) {
        super(name, age);
        this.canFly = canFly;
    }
    
    @Override
    public void makeSound() {
        System.out.println(name + " chirps: Tweet!");
    }
    
    // Method with ternary and if (CC = 3)
    public void fly() {
        String action = canFly ? "flying" : "walking";
        if (canFly) {
            System.out.println(name + " is " + action);
        }
    }
}

// Level 2 from Bird (DIT = 2)
class Eagle extends Bird {
    private double wingspan;
    
    public Eagle(String name, int age, double wingspan) {
        super(name, age, true);
        this.wingspan = wingspan;
    }
    
    @Override
    public void makeSound() {
        System.out.println(name + " screeches!");
    }
    
    // Complex method with multiple conditions (CC = 4)
    public void hunt(String prey) {
        if (prey != null && wingspan > 2.0) {
            if (prey.equals("fish") || prey.equals("rabbit")) {
                System.out.println(name + " hunts " + prey);
            }
        }
    }
}

// Test class
public class ComplexInheritance {
    
    public static void main(String[] args) {
        // Test inheritance hierarchy
        Animal animal = new Dog("Buddy", 3, "Golden Retriever");
        animal.makeSound();
        animal.isAdult();
        animal.getCategory();
        
        Mammal mammal = new Cat("Whiskers", 2, true);
        mammal.makeSound();
        mammal.feed(3);
        
        Dog dog = new Dog("Max", 5, "Labrador");
        dog.makeSound();
        dog.performTricks();
        dog.learnTrick("sit");
        
        Puppy puppy = new Puppy("Tiny", 0, "Beagle");
        puppy.makeSound();
        puppy.train();
        
        Cat cat = new Cat("Fluffy", 1, false);
        cat.makeSound();
        cat.hunt(5);
        
        Bird bird = new Eagle("Thunder", 4, 2.5);
        bird.makeSound();
        bird.fly();
        
        Eagle eagle = (Eagle) bird;
        eagle.hunt("fish");
    }
}

