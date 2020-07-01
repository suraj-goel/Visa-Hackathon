/*
ChatBot to automate inventory management using DiagloFlow
Bot is added in the search page and can perform the following:
1. view all products and product information
2. add products stock
3. remove product stock
 */

'use strict';

const functions = require('firebase-functions');
const {WebhookClient} = require('dialogflow-fulfillment');
const {Card, Suggestion} = require('dialogflow-fulfillment');
const mysql = require('mysql');

process.env.DEBUG = 'dialogflow:debug'; 
 
exports.dialogflowFirebaseFulfillment = functions.https.onRequest((request, response) => {
  const agent = new WebhookClient({ request, response });
  console.log('Dialogflow Request headers: ' + JSON.stringify(request.headers));
  console.log('Dialogflow Request body: ' + JSON.stringify(request.body));
 
  function welcome(agent) {
    agent.add(`Welcome to the Small-Business App!`);
  }
 
  function fallback(agent) {
    agent.add(`I didn't understand`);
    agent.add(`I'm sorry, can you try again?`);
  }
  function connectToDB(){
    const connection = mysql.createConnection({
      host:'SG-visahackathon-2575-master.servers.mongodirector.com',
      user:'sgroot',
      password:'k0fcxBO64qM.A2q1',
      database:'smallBusiness'
    });
    return new Promise((resolve,reject)=>{
      connection.connect();
      console.log('Connection Done');
      resolve(connection);
    });
  }
  function queryGetInventory(connection,merchantID){
  return new Promise((resolve,reject)=>{
    var query = "SELECT * FROM Product WHERE MerchantID = " +"'" + merchantID +"'";
    connection.query(query,(error,results,fields)=>{
      resolve(results);
    });
  });
}

function additemsinDB(connection,merchantID,Name,Quantity){
  return new Promise((resolve,reject)=>{
    var query = "Update Product SET Quantity = Quantity + " + Quantity + " WHERE MerchantID=" + "'" + merchantID + "' AND UPPER(Name) = UPPER('" + Name + "')";
    connection.query(query,function(error,result,fields){
      resolve(result)
    })
  })
}

function decreaseitemsinDB(connection,merchantID,Name,Quantity){
  return new Promise((resolve,reject)=>{
    var query = "Update Product SET Quantity = Quantity - " + Quantity + " WHERE MerchantID=" + "'" + merchantID + "' AND UPPER(Name) = UPPER('" + Name + "')";
    connection.query(query,function(error,result,fields){
      resolve(result)
    })
  })
}

function getProduct(connection,merchantID,Name){
  return new Promise((resolve,reject)=>{
    var query = "SELECT * FROM Product WHERE UPPER(Name) = UPPER('" +Name + "') AND MerchantID =  '" + merchantID +"'";
    connection.query(query,function(error,result,fields){
      resolve(result)
    })
  })
}

function authenticate(connection,email,password){
    return new Promise((resolve,reject)=>{
      var query = "SELECT MerchantID FROM Merchant WHERE EmailID="+"'"+email+"'" + " AND Password="+"'"+password+"'";
      // console.log(query)
      connection.query(query,(error,results,fields)=>{
        resolve(results);
      });
    });
  }

  
function handleGetInventory(agent){
  return connectToDB().then(connection=>{
    var email = agent.parameters.email;
    var password = agent.parameters.password;
    return authenticate(connection,email,password).then(result=>{
      
      if(result.length===0){
        agent.add('Credentials Invalid');
        connection.end();
      }
      else{
        return queryGetInventory(connection,result[0].MerchantID).then(result=>{
          var res = "Here's your inventory details: \n";
          
          result.forEach(function(product){
            res+=`${product.Quantity} ${product.Name} items` + ' , ';
            
          });
          agent.add(res)
          connection.end();
        });
      
      }
      
    });
  });
}

function incrementProducts(agent){

  return connectToDB().then(connection=>{
    var email = agent.parameters.email;
    var password = agent.parameters.password;
    var productName = agent.parameters.productName;
    var productQuantity = agent.parameters.productQuantity;
    return authenticate(connection,email,password).then(result=>{
      
      if(result.length===0){
        agent.add('Credentials Invalid');
        connection.end();
      }
      else{
        
        return additemsinDB(connection,result[0].MerchantID,productName,productQuantity).then(result=>{
          var affectedRows = result.affectedRows;
          if(affectedRows===0){
            agent.add('No Such Product Exists');
          }else{
            
            agent.add('Updated Successfully');
          }

        })
        
        connection.end();
        
      
      }
      
    });
  });
}

function decrementProducts(agent){

  return connectToDB().then(connection=>{
    var email = agent.parameters.email;
    var password = agent.parameters.password;
    var productName = agent.parameters.productName;
    var productQuantity = agent.parameters.productQuantity;
    return authenticate(connection,email,password).then(result=>{
      
      if(result.length===0){
        agent.add('Credentials Invalid');
        connection.end();
      }
      else{
        
        return decreaseitemsinDB(connection,result[0].MerchantID,productName,productQuantity).then(result=>{
          var affectedRows = result.affectedRows;
          if(affectedRows===0){
            agent.add('No Such Product Exists');
          }else{
            
            agent.add('Updated Successfully');
          }

        })
        
        connection.end();
        
      
      }
      
    });
  });
}

function getProductDetails(agent){

  return connectToDB().then(connection=>{
    var email = agent.parameters.email;
    var password = agent.parameters.password;
    var productName = agent.parameters.productName;
    
    return authenticate(connection,email,password).then(result=>{
      
      if(result.length===0){
        agent.add('Credentials Invalid');
        connection.end();
      }
      else{
        
        return getProduct(connection,result[0].MerchantID,productName).then(result=>{
          if(result.length){
            var res= "Here's your product details : ";
            result.forEach(function(product){
              res+=`You have ${product.Quantity} ${product.Name} items` + ' , ' + `Description is ${product.Description} `;
              // agent.add(`${product.Quantity} ${product.Name} items`);
            });
            agent.add(res)
          }else{
            agent.add('No Valid Match Found')
          }
        })
        
        connection.end();
        
      
      }
      
    });
  });
}
  
  let intentMap = new Map();
  intentMap.set('Default Welcome Intent', welcome);
  intentMap.set('Default Fallback Intent', fallback);
  intentMap.set('getInventoryDetails', handleGetInventory);
  intentMap.set('incrementProducts', incrementProducts);
  intentMap.set('decrementProducts', decrementProducts);
  intentMap.set('getProductDetails', getProductDetails);

  agent.handleRequest(intentMap);
});
