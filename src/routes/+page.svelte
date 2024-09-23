<script>
  let formData = {};
</script>

<div class="container mx-auto p-8">
  <h1 class="text-2xl font-bold mb-8">Form Inputs Example</h1>

  <form class="space-y-6">
    <!-- Text Input -->
    <div>
      <label class="block mb-2 text-gray-700">Text Input</label>
      <input type="text" bind:value={formData.textInput} class="w-full p-2 border border-gray-300 rounded-md" placeholder="Enter text"/>
    </div>

    <!-- Password Input -->
    <div>
      <label class="block mb-2 text-gray-700">Password Input</label>
      <input type="password" bind:value={formData.passwordInput} class="w-full p-2 border border-gray-300 rounded-md" placeholder="Enter password"/>
    </div>

    <!-- Email Input -->
    <div>
      <label class="block mb-2 text-gray-700">Email Input</label>
      <input type="email" bind:value={formData.emailInput} class="w-full p-2 border border-gray-300 rounded-md" placeholder="Enter email"/>
    </div>

    <!-- Number Input -->
    <div>
      <label class="block mb-2 text-gray-700">Number Input</label>
      <input type="number" bind:value={formData.numberInput} class="w-full p-2 border border-gray-300 rounded-md" placeholder="Enter number"/>
    </div>

    <!-- Telephone Input -->
    <div>
      <label class="block mb-2 text-gray-700">Telephone Input</label>
      <input type="tel" bind:value={formData.telInput} class="w-full p-2 border border-gray-300 rounded-md" placeholder="Enter telephone"/>
    </div>

    <!-- URL Input -->
    <div>
      <label class="block mb-2 text-gray-700">URL Input</label>
      <input type="url" bind:value={formData.urlInput} class="w-full p-2 border border-gray-300 rounded-md" placeholder="Enter URL"/>
    </div>

    <!-- Date Input -->
    <div>
      <label class="block mb-2 text-gray-700">Date Input</label>
      <input type="date" bind:value={formData.dateInput} class="w-full p-2 border border-gray-300 rounded-md"/>
    </div>

    <!-- Time Input -->
    <div>
      <label class="block mb-2 text-gray-700">Time Input</label>
      <input type="time" bind:value={formData.timeInput} class="w-full p-2 border border-gray-300 rounded-md"/>
    </div>

    <!-- Range Input -->
    <div>
      <label class="block mb-2 text-gray-700">Range Input</label>
      <input type="range" bind:value={formData.rangeInput} min="0" max="100" class="w-full"/>
    </div>

    <!-- Checkbox Input -->
    <div>
      <label class="block mb-2 text-gray-700">Checkbox Input</label>
      <input type="checkbox" bind:checked={formData.checkboxInput} class="mr-2"/> Agree to terms
    </div>

    <!-- Radio Input -->
    <div>
      <label class="block mb-2 text-gray-700">Radio Input</label>
      <input type="radio" bind:group={formData.radioInput} value="Option 1" class="mr-2"/> Option 1
      <input type="radio" bind:group={formData.radioInput} value="Option 2" class="ml-4 mr-2"/> Option 2
    </div>

    <!-- Select Dropdown -->
    <div>
      <label class="block mb-2 text-gray-700">Select Dropdown</label>
      <select bind:value={formData.selectInput} class="w-full p-2 border border-gray-300 rounded-md">
        <option value="">Choose an option</option>
        <option value="Option 1">Option 1</option>
        <option value="Option 2">Option 2</option>
      </select>
    </div>

    <!-- Textarea -->
    <div>
      <label class="block mb-2 text-gray-700">Textarea</label>
      <textarea bind:value={formData.textareaInput} rows="4" class="w-full p-2 border border-gray-300 rounded-md" placeholder="Enter text"></textarea>
    </div>

    <!-- File Input -->
    <div>
      <label class="block mb-2 text-gray-700">File Input</label>
      <input type="file" bind:files={formData.fileInput} class="w-full p-2 border border-gray-300 rounded-md"/>
    </div>

    <!-- Submit Button -->
    <div>
      <button type="submit" class="px-4 py-2 bg-blue-500 text-white rounded-md">Submit</button>
    </div>
  </form>
</div>

<style>
  .container {
    max-width: 600px;
  }
</style>
