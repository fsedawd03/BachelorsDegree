/*
 * Copyright (c) Microsoft Corporation. All rights reserved. Licensed under the MIT license.
 * See LICENSE in the project root for license information.
 */

/* global Office */

import axios from "axios";

Office.onReady(() => {
  // If needed, Office.js is ready to be called.
});

/**
 * Shows a notification when the add-in command is executed.
 * @param event
 */
async function action(event: Office.AddinCommands.Event) {
  const messageGood: Office.NotificationMessageDetails = {
    type: Office.MailboxEnums.ItemNotificationMessageType.InformationalMessage,
    message: "The email is safe",
    icon: "YesIcon.80x80",
    persistent: true,
  };

  const messageBad: Office.NotificationMessageDetails = {
    type: Office.MailboxEnums.ItemNotificationMessageType.InformationalMessage,
    message: "The email might be an attempt at phishing",
    icon: "NoIcon.80x80",
    persistent: true,
  };

  // Show a notification message.
  //Office.context.mailbox.item.notificationMessages.replaceAsync("ActionPerformanceNotification", messageGood);

  // Be sure to indicate when the add-in command function is complete.
  // Get the headers of the message
  Office.context.mailbox.item.getAllInternetHeadersAsync(function getCallbackHeaders(
    asyncResult: Office.AsyncResult<any>
  ): void {
    if (asyncResult.status === Office.AsyncResultStatus.Succeeded) {
      let headersResponse: string;
      headersResponse = asyncResult.value;
      // Get the html code of the message
      Office.context.mailbox.item.body.getAsync(
        Office.CoercionType.Html,
        function getCallbackBody(asyncResult: Office.AsyncResult<any>): void {
          if (asyncResult.status === Office.AsyncResultStatus.Succeeded) {
            let body: string = asyncResult.value;
            // Get the text of the message
            Office.context.mailbox.item.body.getAsync(
              Office.CoercionType.Text,
              function getCallbackText(asyncResult: Office.AsyncResult<any>): void {
                if (asyncResult.status === Office.AsyncResultStatus.Succeeded) {
                  let message: EmailMessage;
                  let textMessage: string = asyncResult.value;
                  message = {
                    email: Office.context.mailbox.userProfile.emailAddress,
                    emailBody: body,
                    emailHeaders: headersResponse,
                    emailMessage: textMessage,
                  };
                  console.log(headersResponse);
                  axios
                    .post("http://localhost:6500/v1.0/phishing/runModel", message)
                    .then((response) => {
                      console.log(response.data);
                      if (response.data == 1) {
                        console.log("False");
                        Office.context.mailbox.item.notificationMessages.replaceAsync(
                          "ActionPerformanceNotification",
                          messageBad
                        );
                      } else if (response.data == 0) {
                        console.log("True");
                        Office.context.mailbox.item.notificationMessages.replaceAsync(
                          "ActionPerformanceNotification",
                          messageGood
                        );
                      }
                      event.completed();
                    })
                    .catch((error) => {
                      if (error.response) {
                        console.log(error.response.data);
                      }
                      event.completed();
                    });
                } else {
                  console.log("Error getting the body text: " + asyncResult.error.message);
                  event.completed();
                }
              }
            );
            //
          } else {
            console.log("Error getting the body: " + asyncResult.error.message);
            event.completed();
          }
        }
      );
      //
    } else {
      console.log("Error getting selected headers: " + asyncResult.error.message);
      event.completed();
    }
  });
}

class EmailMessage {
  email: string;
  emailHeaders;
  emailBody: string;
  emailMessage: string;
}

// Register the function with Office.
Office.actions.associate("action", action);
