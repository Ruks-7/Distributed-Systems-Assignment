// Connect to MongoDB
const databaseName = 'contact_system';
const db = db.getSiblingDB(databaseName);

// Drop existing collections (optional, for development)
db.users.drop();
db.contacts.drop();

// Create users collection
db.createCollection('users', {
    validator: {
        $jsonSchema: {
            bsonType: 'object',
            required: ['username', 'password', 'email'],
            properties: {
                username: {
                    bsonType: 'string',
                    description: 'must be a string and is required'
                },
                password: {
                    bsonType: 'string',
                    description: 'must be a string and is required'
                },
                email: {
                    bsonType: 'string',
                    description: 'must be a string and is required',
                    pattern: "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
                }
            }
        }
    }
});

// Create contacts collection
db.createCollection('contacts', {
    validator: {
        $jsonSchema: {
            bsonType: 'object',
            required: ['mobile', 'email', 'address', 'registration_number', 'user_id'],
            properties: {
                mobile: {
                    bsonType: 'string',
                    description: 'must be a string and is required'
                },
                email: {
                    bsonType: 'string',
                    description: 'must be a string and is required',
                    pattern: "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
                },
                address: {
                    bsonType: 'string',
                    description: 'must be a string and is required'
                },
                registration_number: {
                    bsonType: 'string',
                    description: 'must be a string and is required'
                },
                user_id: {
                    bsonType: 'objectId',
                    description: 'must be an objectId and is required'
                }
            }
        }
    }
});

// Create indexes
db.users.createIndex({ username: 1 }, { unique: true });
db.contacts.createIndex({ registration_number: 1 }, { unique: true });

// Insert sample users
db.users.insertMany([
    {
        username: 'john_doe',
        password: 'password123',
        email: 'john@example.com'
    },
    {
        username: 'jane_doe',
        password: 'password456',
        email: 'jane@example.com'
    }
]);

// Insert sample contacts (replace user_id with actual ObjectId)
const users = db.users.find().toArray();
const user1Id = users[0]._id;
const user2Id = users[1]._id;

db.contacts.insertMany([
    {
        mobile: '123-456-7890',
        email: 'contact1@example.com',
        address: '123 Main St',
        registration_number: 'REG001',
        user_id: user1Id
    },
    {
        mobile: '987-654-3210',
        email: 'contact2@example.com',
        address: '456 Oak Ave',
        registration_number: 'REG002',
        user_id: user2Id
    }
]);

// Find all users
print("All Users:");
db.users.find().forEach(printjson);

// Find all contacts
print("\nAll Contacts:");
db.contacts.find().forEach(printjson);

// Find contacts by registration number
print("\nContact with registration number REG001:");
db.contacts.find({ registration_number: 'REG001' }).forEach(printjson);