package com.legacy.system;

// Livello 0: Object (implicito)

// Livello 1
class AbstractSystemBase {
    protected int baseId;
}

// Livello 2
class CoreEntity extends AbstractSystemBase {
    protected String entityName;
}

// Livello 3
class BusinessObject extends CoreEntity {
    protected double value;
}

// Livello 4
class TransactionHandler extends BusinessObject {
    public void handle() {}
}

// Livello 5
class AbstractProcessor extends TransactionHandler {
    public void process() {}
}

// Livello 6 (Questa classe avrà DIT = 6 -> Allarme Rosso)
// Ha anche NOC = 2 (ha due figli)
class BaseManager extends AbstractProcessor {
    public void manage() {}
}

// Figli per aumentare il NOC di BaseManager
class UserManager extends BaseManager {}
class ProductManager extends BaseManager {}