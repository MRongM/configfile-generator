<template>
  <div class="container">
    <img src="/banner.png" alt="wordcloud" class="logo-banner" />
    <div class="search-area">
      <input
        ref="searchInput"
        v-model="query"
        class="search-box"
        placeholder="Search files..."
        @input="onInput"
        @keydown.down.prevent="moveDown"
        @keydown.up.prevent="moveUp"
        @keydown.enter.prevent="selectItem"
      />

      <ul v-if="filtered.length && query" class="suggestions">
        <li
          v-for="(item, index) in filtered"
          :key="item.name"
          :class="{ active: index === selectedIndex }"
          @click="openFile(item)"
        >
          {{ item.name }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import files from './files.js';

export default {
  data() {
    return {
      query: '',
      selectedIndex: -1,
      files
    };
  },
  mounted() {
    this.$refs.searchInput.focus()
  },

  computed: {
    filtered() {
      return this.files.filter(file =>
        file.name.toLowerCase().includes(this.query.toLowerCase())
      );
    }
  },
  methods: {
    onInput() {
      this.selectedIndex = -1;
    },
    moveDown() {
      if (this.selectedIndex < this.filtered.length - 1) {
        this.selectedIndex++;
      }
    },
    moveUp() {
      if (this.selectedIndex > 0) {
        this.selectedIndex--;
      }
    },
    selectItem() {
      if (this.filtered[this.selectedIndex]) {
        this.openFile(this.filtered[this.selectedIndex]);
      }
    },
    openFileAsSafeTextTab(fileUrl) {
      fetch(fileUrl)
        .then((res) => {
          if (!res.ok) throw new Error('Load file failed');
          return res.text();
        })
        .then((text) => {
          const win = window.open('', '_blank');
          if (!win) {
            alert('Please allow new tab page');
            return;
          }

          const doc = win.document;
          doc.open();
          doc.write(`
            <!DOCTYPE html>
            <html>
              <head>
                <title>Preview</title>
                <style>
                  body {
                    margin: 0;
                    padding: 1em;
                    font-family: monospace;
                    background: #f9f9f9;
                  }
                  pre {
                    white-space: pre-wrap;
                    word-wrap: break-word;
                  }
                </style>
              </head>
              <body>
              </body>
            </html>
          `);
          doc.close();

          const pre = doc.createElement('pre');
          pre.textContent = text;
          doc.body.appendChild(pre);
        })
        .catch((err) => {
          alert('Open file error：' + err.message);
        });
    },
    openFile(file) {
      if (import.meta.env.MODE === 'development') {
        window.open(file.url, '_blank');
      } else {
        this.openFileAsSafeTextTab(file.url);
      }
    }
  }
};
</script>

<style scoped>
.logo-banner {
  max-width: 550px;
  width: 100%;
  margin-bottom: 40px;
  display: block;
}

.container {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  min-height: 100vh;
  background: #fff;
}

.search-area {
  width: 100%;
  max-width: 600px;
  text-align: center;
  position: relative;
}

.search-box {
  width: 100%;
  padding: 14px 20px;
  margin-bottom: 50vh;
  font-size: 18px;
  border: 1px solid #dfe1e5;
  border-radius: 24px;
  outline: none;
  transition: box-shadow 0.2s ease;
}

.search-box:focus {
  box-shadow: 0 1px 6px rgba(32, 33, 36, 0.28);
  border-color: transparent;
}

.suggestions {
  position: absolute;
  top: 60px;
  left: 0;
  right: 0;
  margin: 0 auto;
  background: #fff;
  border: 1px solid #dfe1e5;
  border-radius: 8px;
  list-style: none;
  padding: 0;
  max-height: 200px;
  overflow-y: auto;
  z-index: 10;
}

.suggestions li {
  padding: 12px 20px;
  cursor: pointer;
}

.suggestions li:hover,
.suggestions li.active {
  background-color: #f1f3f4;
}
</style>
