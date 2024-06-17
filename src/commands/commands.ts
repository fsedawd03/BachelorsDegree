/*
 * Copyright (c) Microsoft Corporation. All rights reserved. Licensed under the MIT license.
 * See LICENSE in the project root for license information.
 */

/* global Office */

Office.onReady(() => {
  // If needed, Office.js is ready to be called.
});

/**
 * Shows a notification when the add-in command is executed.
 * @param event
 */
async function action(event: Office.AddinCommands.Event) {
  const message: Office.NotificationMessageDetails = {
    type: Office.MailboxEnums.ItemNotificationMessageType.InformationalMessage,
    message: "Performed action",
    icon: "Icon.80x80",
    persistent: true,
  };

  // Show a notification message.
  Office.context.mailbox.item.notificationMessages.replaceAsync("ActionPerformanceNotification", message);

  // Be sure to indicate when the add-in command function is complete.
  // Get the headers of the message
  Office.context.mailbox.item.getAllInternetHeadersAsync(function getCallbackHeaders(
    asyncResult: Office.AsyncResult<any>
  ): void {
    if (asyncResult.status === Office.AsyncResultStatus.Succeeded) {
      let headersResponse: string;
      headersResponse = JSON.stringify(asyncResult.value);
      // Get the html code of the message
      Office.context.mailbox.item.body.getAsync(
        Office.CoercionType.Html,
        function getCallbackBody(asyncResult: Office.AsyncResult<any>): void {
          if (asyncResult.status === Office.AsyncResultStatus.Succeeded) {
            let body: string = JSON.stringify(asyncResult.value);
            // Get the text of the message
            Office.context.mailbox.item.body.getAsync(
              Office.CoercionType.Text,
              function getCallbackText(asyncResult: Office.AsyncResult<any>): void {
                if (asyncResult.status === Office.AsyncResultStatus.Succeeded) {
                  let message: EmailMessage;
                  let textMessage: string = JSON.stringify(asyncResult.value);
                  message = {
                    email: Office.context.mailbox.userProfile.emailAddress,
                    emailBody: body,
                    emailHeaders: headersResponse,
                    emailMessage: textMessage,
                  };
                  console.log(message.emailBody);
                  event.completed();
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
  emailHeaders: string;
  emailBody: string;
  emailMessage: string;
}

// Register the function with Office.
Office.actions.associate("action", action);
