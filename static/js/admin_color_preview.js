/**
 * LFIS Admin – Live color swatch preview
 * Shows a colored circle next to hex color input fields in SiteSettings.
 */
(function () {
    'use strict';

    function hexToValid(val) {
        val = val.trim();
        if (/^#[0-9a-fA-F]{6}$/.test(val)) return val;
        if (/^#[0-9a-fA-F]{3}$/.test(val)) return val;
        return null;
    }

    function attachSwatch(input) {
        if (input.dataset.swatchAttached) return;
        input.dataset.swatchAttached = 'true';

        // Wrap in flex row
        const wrapper = document.createElement('div');
        wrapper.className = 'color-swatch-row';
        input.parentNode.insertBefore(wrapper, input);
        wrapper.appendChild(input);

        // Create swatch element
        const swatch = document.createElement('span');
        swatch.className = 'color-preview-swatch';
        swatch.title = 'Live preview';
        wrapper.appendChild(swatch);

        // Create native color picker
        const picker = document.createElement('input');
        picker.type = 'color';
        picker.title = 'Pick a color';
        picker.style.cssText = 'border:none;background:none;cursor:pointer;width:36px;height:36px;';
        wrapper.appendChild(picker);

        function updateSwatch(hex) {
            const valid = hexToValid(hex);
            if (valid) {
                swatch.style.background = valid;
                swatch.style.borderColor = valid;
                picker.value = valid;
            } else {
                swatch.style.background = '#eee';
                swatch.style.borderColor = '#ddd';
            }
        }

        // Sync hex input → swatch & picker
        input.addEventListener('input', () => updateSwatch(input.value));
        input.addEventListener('change', () => updateSwatch(input.value));

        // Sync picker → hex input & swatch
        picker.addEventListener('input', () => {
            input.value = picker.value;
            updateSwatch(picker.value);
        });

        // Initialize
        updateSwatch(input.value);
    }

    function init() {
        // Target color fields in SiteSettings form
        document.querySelectorAll('input[name="primary_color"], input[name="secondary_color"]').forEach(attachSwatch);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
