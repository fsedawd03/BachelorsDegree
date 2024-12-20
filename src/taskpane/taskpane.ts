/*
 * Copyright (c) Microsoft Corporation. All rights reserved. Licensed under the MIT license.
 * See LICENSE in the project root for license information.
 */

/* global document, Office */

Office.onReady((info) => {
  if (info.host === Office.HostType.Outlook) {
    document.getElementById("sideload-msg").style.display = "none";
    document.getElementById("app-body").style.display = "flex";
    document.getElementById("run").onclick = run;
  }
  Office.context.mailbox.item.getAllInternetHeadersAsync((asyncResult) => {
    if (asyncResult.status === Office.AsyncResultStatus.Succeeded) {
      console.log("Selected headers: " + JSON.stringify(asyncResult.value));
    } else {
      console.log("Error getting selected headers: " + JSON.stringify(asyncResult.error));
    }
  });
});

export async function run() {
  /**
   * Insert your Outlook code here
   */

  const item = Office.context.mailbox.item;
  document.getElementById("item-subject").innerHTML = "<b>Subject:</b> <br/>" + item.subject;
}
