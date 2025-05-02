# Unused CSS class checker
A simple Python-based tool to check for loaded but unused CSS classes in rendered HTML.
Edit: I'm not sure exactly how it does differ from other tools. Just for my own use case and sites I compared it to, it seemed to be more accurate. Some seem to check the database. Others go straight to actually removing the classes - but that can be overkill, or unhelpful for people using builders with classes that can be deactivated alongside any associated JS. I use the sitemap to do a crawl. Works for me, at least.

## Dependencies
beautifulsoup4: Required to parse and extract data from the HTML and sitemaps (at least in my case, it worked fine without creating more dependencies).
requests: Required to make HTTP requests to fetch the pages and the CSS.

## To install those dependencies, assuming Python is already set up
pip install requests beautifulsoup4

----

# To use
I kept things simple. I also didn't want to put another flexible scraper into the world.

## Set sitemap and site-wide universal CSS locations to compare here
main_sitemap_url = 'https://yourdomain.com/sitemap.xml'
css_url = 'https://yourdomain.com/wp-content/uploads/oxygen/css/universal.css'

## The caveat
It doesn't check dynamically inserted classes and JavaScript content. That would be a bit of a can of worms. Probably doable, but I didn't need it. Anyone wanting to add it is welcome to and you'll be credited.

----

## Why I made it
Existing tools weren't working that well for me. Many seemed to focus more on the database, not what is actually rendered. This may not be suitable for your site, either - especially if you have a lot of dynamically inserted content. But that's not great for SEO and usability, anyway, so maybe rethink that. :)

## Ideal use case
Websites with a central CSS file for a lot of your CSS. This may be generated largely by a theme. It could be particularly helpful in commonly used builders such as Bricks, Elementor, or Avada, where elements can be manually activated and removed from the theme.

## My own use case
Ridiculously optimised websites built in Oxygen Classic. I'm trying to experiment to see if I can strip out even more of the default CSS than I already have, so I can essentially use it as my personal visual builder with nothing but code blocks, images, divs, sections, headings, and text boxes.

---

## Special licence terms
See the notes on the licence tab. Commercial use by companies to improve their own websites is fine. Reselling or redistributing without credit is not. Where there is ambiguity here, the licence notes take precedent.
