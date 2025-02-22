#!/usr/bin/python3
""" """
import sys
from models.base_model import BaseModel
import unittest
import datetime
from uuid import UUID
import json
import os


class test_basemodel(unittest.TestCase):
    """Test class for BaseModel"""

    def __init__(self, *args, **kwargs):
        """Initialize test class"""
        super().__init__(*args, **kwargs)
        self.name = 'BaseModel'
        self.value = BaseModel

    def setUp(self):
        """Set up test"""
        pass

    def tearDown(self):
        """Tear down test"""
        try:
            os.remove('file.json')
        except BaseException:
            pass

    def test_default(self):
        """Test default instances"""
        i = self.value()
        self.assertEqual(type(i), self.value)

    def test_kwargs(self):
        """Test instance with kwargs"""
        i = self.value()
        copy = i.to_dict()
        new = BaseModel(**copy)
        self.assertIsNot(new,i)

    def test_kwargs_int(self):
        """Test instance with kwargs as integers"""
        i = self.value()
        copy = i.to_dict()
        copy.update({1: 2})
        with self.assertRaises(TypeError):
            BaseModel(**copy)

    def test_init_with_invalid_kwargs(self):
        """Test that initializing a BaseModel instance
        with invalid keyword arguments fails correctly."""
        kwargs = {
            "id": "invalid-id",
            "created_at": "invalid-created-at",
            "updated_at": "invalid-updated-at",
        }

        with self.assertRaises(Exception):
            BaseModel(**kwargs)

    def test_init_without_kwargs(self):
        """Test that initializing a BaseModel instance
        without keyword arguments works correctly."""
        base_model = BaseModel()
        self.assertIsNotNone(base_model.id)
        self.assertTrue(isinstance(base_model.created_at, datetime.datetime))
        self.assertTrue(isinstance(base_model.updated_at, datetime.datetime))

    def test_save(self):
        """ Test instance save method"""
        i = self.value()
        i.save()
        key = self.name + "." + i.id
        with open('file.json', 'r') as f:
            j = json.load(f)
            self.assertEqual(j[key], i.to_dict())

    def test_str(self):
        """ Test instance string representation"""
        i = self.value()
        self.assertEqual(str(i), '[{}] ({}) {}'.format(self.name, i.id,
                         i.__dict__))

    def test_todict(self):
        """Test instance to_dict method """
        i = self.value()
        n = i.to_dict()
        self.assertEqual(i.to_dict(), n)

    def test_kwargs_none(self):
        """ Test instance with kwargs as None"""
        n = {None: None}
        with self.assertRaises(TypeError):
            new = self.value(**n)

    def test_id(self):
        """ Test instance ID type"""
        new = self.value()
        self.assertEqual(type(new.id), str)

    def test_two_ids(self):
        bm1 = BaseModel()
        bm2 = BaseModel()
        self.assertNotEqual(bm1.id, bm2.id)

    def test_created_at(self):
        """ Test instance creation time"""
        new = self.value()
        self.assertEqual(type(new.created_at), datetime.datetime)

    def test_updated_at(self):
        """ Test instance update time"""
        new = self.value()
        self.assertEqual(type(new.updated_at), datetime.datetime)
        n = new.to_dict()
        new = BaseModel(**n)
        self.assertFalse(new.created_at == new.updated_at)

if __name__ == '__main__':
    unittest.main()
