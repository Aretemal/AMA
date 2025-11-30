import js from "@eslint/js";
import globals from "globals";
import tseslint from "typescript-eslint";
import pluginVue from "eslint-plugin-vue";
import prettier from "eslint-config-prettier";

export default [
  // eslint:recommended
  { files: ["**/*.{js,mjs,cjs,ts,mts,cts,vue}"], ...js.configs.recommended, languageOptions: { globals: globals.browser } },
  ...tseslint.configs.recommended,
  // plugin:vue/vue3-essential
  ...pluginVue.configs["flat/essential"],
  {
    files: ["**/*.vue"],
    languageOptions: {
      parserOptions: {
        parser: tseslint.parser,
      },
    },
  },
  // Отключаем правила форматирования ESLint, чтобы не конфликтовать с Prettier
  prettier,
  // Ваши кастомные правила
  {
    files: ["**/*.{js,ts,vue}"],
    rules: {
      // Автоматически исправляет неиспользуемые переменные
      '@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
      'no-unused-vars': 'off', // Отключаем базовое правило, используем TypeScript версию
      // Примеры других правил:
      // 'no-console': 'warn', // Предупреждение при использовании console
      // 'prefer-const': 'error', // Ошибка, если можно использовать const вместо let
      // 'no-var': 'error', // Запретить использование var
    },
  },
  {
    ignores: ["dist/**", "node_modules/**", "*.config.*"],
  },
];
