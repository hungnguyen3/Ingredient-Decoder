const { expect } = require("@jest/globals");
const { report } = require("superagent");
const request = require("supertest");
var {app} = require("./backend");


describe("login_test", () => {              // tests for /login
  test("clogin", done => {                  // test for logining in a customer account
    let postdata_c = {username: "customer1", password: "123"};
    request(app)
      .post('/login')
      .send(postdata_c)
      .then(response => {
        expect(response.text).toBe("{\"message\":\"clogin\"}");
        expect(response.statusCode).toBe(200);
        done();
      }); 
  });
  test("slogin", done => {              // test for logining in a store owner account
    let postdata_s = {username: "storeowner1", password: "123"};
    request(app)
      .post('/login')
      .send(postdata_s)
      .then(response => {
        expect(response.text).toBe("{\"message\":\"slogin\"}");
        expect(response.statusCode).toBe(200);
        done();
      });
  });
});

describe("signup_test", () => {             //tests for /signup
    test("signup_c", done => {              // test for signing up a a customer account
      let postdata_c = {username: "customer1", password: "123", type: "c", itemlist: []};
      request(app)
        .post('/signup')
        .send(postdata_c)
        .then(response => {
          expect(response.text).toBe("{\"message\":\"sign up successfully\"}");
          expect(response.statusCode).toBe(200);
          done();
        }); 
    });
    test("signup_s", done => {              // test for signing up a store owner account
      let postdata_s = {username: "storeowner1", password: "123", type: "s", itemlist: []};
      request(app)
        .post('/signup')
        .send(postdata_s)
        .then(response => {
          expect(response.text).toBe("{\"message\":\"sign up successfully\"}");
          expect(response.statusCode).toBe(200);
          done();
        });
    });
});

describe("plist_test", () => {             // tests for /plist, /plist_add, /plist_clear
    test("plist", done => {                // test for geting the plist of current user
      let postdata_c = {username: "customer1"};
      request(app)
        .post('/plist')
        .send(postdata_c)
        .then(response => {
          expect(response.text).toBe("{\"message\":\"[]\"}");
          expect(response.statusCode).toBe(200);
          done();
        }); 
    });
    test("plist_add", done => {             // test for adding a new item in plist
        let postdata_c = {username: "customer1", plist_add:"milk"};
      request(app)
        .post('/plist_add')
        .send(postdata_c)
        .then(response => {
          expect(response.text).toBe("{\"message\":\"plist_add\"}");
          expect(response.statusCode).toBe(200);
          done();
        });
    });
    test("plist_clear", done => {               // test for clearing the plist
        let postdata_c = {username: "customer1"};
        request(app)
          .post('/plist_clear')
          .send(postdata_c)
          .then(response => {
            expect(response.text).toBe("{\"message\":\"plist_add\"}");
            expect(response.statusCode).toBe(200);
            done();
          });
      });

});



describe("ilist_test", () => {                  // tests for /ilist, /ilist_add, /ilist_clear
    test("ilist", done => {                       // test for geting the ilist of current user
      let postdata_s = {username: "storeowner1"};
      request(app)
        .post('/ilist')
        .send(postdata_s)
        .then(response => {
          expect(response.text).toBe("{\"message\":\"[]\"}");
          expect(response.statusCode).toBe(200);
          done();
        }); 
    });
    test("ilist_add", done => {                 // test for adding a new item in ilist, including its name, list, image, and owner
        let postdata_s = {username: "storeowner1", item_name:"apple", item_list:"water, sugar", item_image:"%%%$$$$####", owner: "storeowner1"};
      request(app)
        .post('/ilist_add')
        .send(postdata_s)
        .then(response => {
          expect(response.text).toBe("{\"message\":\"ilist_add\"}");
          expect(response.statusCode).toBe(200);
          done();
        });
    });
    test("ilist_clear", done => {                  // test for clearing the ilist     
        let postdata_s = {username: "storeowner1"};
        request(app)
          .post('/ilist_clear')
          .send(postdata_s)
          .then(response => {
            expect(response.text).toBe("{\"message\":\"ilist_clear\"}");
            expect(response.statusCode).toBe(200);
            done();
          });
      });

});

describe("search", () => {                          // tests for /byname
    test("search_byname", done => {                     // test for searching by owner's name
      let postdata = {to_search: "storeowner1"};
      request(app)
        .post('/search_byname')
        .send(postdata)
        .then(response => {
          expect(response.text).toBe("{\"message\":\"[apple]\"}");
          expect(response.statusCode).toBe(200);
          done();
        }); 
    });
    test("search_byname", done => {                 // test for searching by item's name
        let postdata = {to_search: "apple"};
        request(app)
          .post('/search_byname')
          .send(postdata)
          .then(response => {
            expect(response.text).toBe("{\"message\":\"[apple]\"}");
            expect(response.statusCode).toBe(200);
            done();
          }); 
      });


});

describe("compare to plist", () => {            // test for compare user's plist to text detection result
    test("compareplist", done => {
      let postdata = {username: "customer1", text_d: "MILK, sugar"};
      request(app)
        .post('/compareplist')
        .send(postdata)
        .then(response => {
          expect(response.text).toBe("{\"message\":\"[milk]\"}");
          expect(response.statusCode).toBe(200);
          done();
        }); 
    });

});



