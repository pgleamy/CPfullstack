<script lang="ts">
  import { EditorTheme, SvelteEditor } from '@nextlint/svelte';

  let editor = SvelteEditor;
</script>

<EditorTheme
  override={{
    '--editor-font': "Söhne, ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, Ubuntu, Cantarell, 'Noto Sans', sans-serif, 'Helvetica Neue', Arial, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol', 'Noto Color Emoji'",
    '--editor-font-code': '"Söhne Mono", Monaco, "Andale Mono", "Ubuntu Mono", monospace',
    '--editor-font-size': '14px',
    '--editor-font-height': '13px',
    '--editor-block-gap': '4px',
    '& .ProseMirror': {
      '& blockquote': {
        backgroundColor: 'teal',
        boxShadow: '0px 4px 12px rgba(0, 0, 0, 0.1)'
      },
      '& pre': {
        backgroundColor: '#000',
        fontFamily: '"Söhne Mono", Monaco, "Andale Mono", "Ubuntu Mono", monospace'
      }
    }
  }}
>
  <SvelteEditor
    content={''}
    placeholder="."
    onCreated={createdEditor => { editor = createdEditor }}
    onChange={nextEditor => { editor = nextEditor }}
  />
</EditorTheme>

