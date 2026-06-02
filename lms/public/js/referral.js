// lms/public/js/referral.js

document.addEventListener("DOMContentLoaded", function() {
    const urlParams = new URLSearchParams(window.location.search);
    const refCode = urlParams.get('ref');
    
    if (refCode) {
        frappe.call({
            method: "lms.lms.referral.track_referral_click",
            args: {
                ref_code: refCode
            },
            callback: function(r) {
                if (!r.exc) {
                    console.log("Referral intent tracked.");
                }
            }
        });
    }
});
