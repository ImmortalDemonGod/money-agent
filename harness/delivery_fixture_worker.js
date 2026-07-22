export default {
  fetch() {
    return new Response(
      "money-agent Stripe test-mode delivery fixture\n\nThis complete artifact exists only to verify the pay-to-deliver seam. It is intentionally static, public, and larger than the delivery probe's minimum artifact floor. A successful test checkout redirects here, proving that the provider's configured completion target is available before the payment surface is considered sellable.\n",
      { headers: { "content-type": "text/plain; charset=utf-8", "cache-control": "no-store" } },
    );
  },
};
