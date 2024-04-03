return {
  {
    "stevearc/conform.nvim",
    -- event = 'BufWritePre', -- uncomment for format on save
    config = function()
      require "configs.conform"
    end,
  },

  -- {
  --   "nvim-tree/nvim-tree.lua",
  --   opts = {
  --     git = { enable = true },
  --   },
  -- },

  {
    "IogaMaster/neocord",
    event = "VeryLazy",
  },

  {
  	"williamboman/mason.nvim",
  	opts = {
  		ensure_installed = {
  			"lua-language-server", "stylua",
  			"html-lsp", "css-lsp" , "prettier"
  		},
  	},
  },

  {
    "hrsh7th/nvim-cmp",
    dependencies = {
      "hrsh7th/cmp-emoji",
    },
    ---@param opts cmp.ConfigSchema
    opts = function(_, opts)
      local has_words_before = function()
        unpack = unpack or table.unpack
        local line, col = unpack(vim.api.nvim_win_get_cursor(0))
        return col ~= 0 and vim.api.nvim_buf_get_lines(0, line - 1, line, true)[1]:sub(col, col):match("%s") == nil
      end

      local luasnip = require("luasnip")
      local cmp = require("cmp")
      opts.sources = cmp.config.sources(vim.list_extend(opts.sources, { { name = "emoji" } }))

      opts.completion = {
        completeopt = "menu,menuone,noinsert,noselect,preview",
      }

      opts.mapping = vim.tbl_extend("force", opts.mapping, {
        ["<CR>"] = cmp.mapping.confirm({ select = false }),
        ["<Tab>"] = cmp.mapping(function(fallback)
          if cmp.visible() then
            cmp.select_next_item()
          -- You could replace the expand_or_jumpable() calls with expand_or_locally_jumpable()
          -- they way you will only jump inside the snippet region
          elseif luasnip.expand_or_jumpable() then
            luasnip.expand_or_jump()
          elseif has_words_before() then
            cmp.complete()
          else
            fallback()
          end
        end, { "i", "s" }),
        ["<S-Tab>"] = cmp.mapping(function(fallback)
          if cmp.visible() then
            cmp.select_prev_item()
          elseif luasnip.jumpable(-1) then
            luasnip.jump(-1)
          else
            fallback()
          end
        end, { "i", "s" }),
      })
    end,
    lazy = false
  },

  -- {
  --   "hrsh7th/nvim-cmp",
  --   opts = {
  --       preselect = cmp.PreselectMode.None,
  --       completion = { completeopt = "menu,menuone,noselect" },    
  --   },
  -- },

  -- {
  --   "L3MON4D3/LuaSnip",
  --   keys = function()
  --     return {}
  --   end,
  -- },

  -- {
  --   "hrsh7th/nvim-cmp",
  --   opts = {
  --     mapping = {
  --       ["<CR>"] = cmp.mapping.confirm {
  --         behavior = cmp.ConfirmBehavior.Insert,
  --         -- when true, auto-selects the first item if nothing was selected,
  --         -- making noselect below not take effect.
  --         select = false,
  --       },
  --     },
  --     -- adding noselect compared to default, to prevent autocomplete when typing,
  --     -- and this is actually nvim-cmp defaults, but NvChad overrides this.
  --     completion = {
  --       completeopt = "menu,menuone,noselect",
  --     },
  --     -- for LSPs that (re)enable this:
  --     preselect = cmp.PreselectMode.None,
  --   },
  -- },

  -- These are some examples, uncomment them if you want to see them work!
  -- {
  --   "neovim/nvim-lspconfig",
  --   config = function()
  --     require("nvchad.configs.lspconfig").defaults()
  --     require "configs.lspconfig"
  --   end,
  -- },
  --
  --
  -- {
  -- 	"nvim-treesitter/nvim-treesitter",
  -- 	opts = {
  -- 		ensure_installed = {
  -- 			"vim", "lua", "vimdoc",
  --      "html", "css"
  -- 		},
  -- 	},
  -- },
}
