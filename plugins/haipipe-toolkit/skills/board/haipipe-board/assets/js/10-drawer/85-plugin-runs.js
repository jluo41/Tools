/* Runs is no longer a top-level Page plugin.
 *
 * The compatibility route remains available at /_board/runs, while its UI is
 * mounted as Run Workspace inside 🧭 Outline.  Keeping this asset as a
 * deliberate no-op lets older Board bundles load without registering a fourth
 * competing surface.
 */
(function () {
  'use strict';
})();
