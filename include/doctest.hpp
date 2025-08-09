// Conan::ImportStart
#pragma once
// Conan::ImportEnd



/*!
 * @file doctest.hpp
 * @defgroup demo Demo
 *
 * @brief [en] demonstration for file-level description
 *     The file-level docstring uses multi-lined code-block with start of  "/*!".
 * @brief [zh] 文件级说明演示
 *     文件级字符串使用形如“/*!”为开始的多行代码块注释。
 *
 * @section tag_1st main-title
 *     Description for the 1st level section. No language tag here means this part will
 *     be visible by all language versions.
 *
 * @subsection tag_2nd [en] sub-title
 *     Description for the 2nd level section. English version for this part.
 * @subsection tag_2nd [zh] 二级目录
 *     关于次级目录的描述。该部分使用中文。
 *
 * @subsubsection tag_3rd_1 figure-addition
 *     You can attach your figure here. Pay attention that the figure you want to include should
 *     be named with 'IN_' or 'ALL_' prefix.
 *     @anchor demo_img_tag
 *     @image html IN_icon2.jpg "Figure Caption"
 *     @note Doxygen and Sphinx are both supported in this system. 'IN_' prefix figures for
 *           Doxygen exclusively; 'OUT_' for Sphinx; and 'ALL_' for both.
 * @subsubsection tag_3rd_2 graph-addition
 *     Also you can create graph with 'DOT' syntax. if your program has complicated calling
 *     logic, this feature affords your user an explicit concept.
 *     @dot
 *     digraph CallFlow {
 *         rankdir=LR;
 *         Compile -> Build [label="to"];
 *         Build -> Clean [label="to"];
 *     }
 *     @enddot
 * @subsubsection tag_3rd_3 formula-addition
 *     Formula can also be defined like:
 *     \f[
 *     f(x) = \frac{1}{\sigma\sqrt{2\pi}} e^{-\frac{(x-\mu)^2}{2\sigma^2}}
 *     \f]
 *     Where:
 *     - \f$\mu\f$ is for mean
 *     - \f$\sigma\f$ is for standard error
 * @subsubsection tag_3rd_4 cross-reference
 *     You can cite to your customized @ref demo_img_tag "anchor", or to the section
 *     @ref tag_1st "tag".
 *
 * @author Chen Zhang <chen.zhang_06sept@foxmail.com>
 * @since 1.0
 */



/**
 * @brief [en] Performs an in-place transformation on each element of a container.
 *
 *     Applies the given function object 'f' to each element in the container 'a'.
 *     The transformation is performed in-place, meaning the original elements
 *     within the container are modified directly. The function object 'f' should
 *     accept a reference to the element type (or a type it can bind to) to allow
 *     modification.
 *
 * @brief [zh] 对容器中的每个元素进行原地转换操作。
 *
 *     将给定的函数对象‘f’应用于容器‘a’中的每个元素。此转换是原地进行的，即容器内的原始元素会被直接修改。
 *     函数对象‘f’应接受对元素类型的引用（或其能够绑定的类型）以便进行修改。
 *
 * @tparam T [en] The type of the container. Must be iterable (support range-based for loop).
 * @tparam T [zh] 容器的类型。必须是可迭代的（支持基于范围的 for 循环）。
 * @tparam F [en] The type of the function object (e.g., lambda, function pointer, functor).
 *                The function object should take a parameter that can bind to a reference
 *                of the container's element type.
 * @tparam F [zh] 函数对象的类型（例如，lambda 表达式、函数指针、函数对象）。
 *                该函数对象应当接受一个参数，该参数能够与容器元素类型的引用进行绑定。
 *
 * @param a [en] The container whose elements are to be transformed. The container is
 *               modified directly (in-place).
 * @param a [zh] 要进行转换的容器。该容器将被直接修改（即原地修改）。
 * @param f [en] The function object (unary callable) to be applied to each element
 *               of the container. This function is responsible for performing the
 *               desired transformation on each element.
 * @param f [zh] 要应用于容器中每个元素的函数对象（单参数可调用对象）。此函数负责对每个元素执行所需的转换操作。
 *
 * @return [en] A copy of the modified container `a`.
 * @return [zh] 修改后的容器‘a’的副本。
 *
 * @note [en] This function modifies the original container `a`. If you wish to avoid
 *            the overhead of copying the container upon return, consider modifying
 *            the return type to `T&` and returning a reference instead.
 * @note [zh] 此函数会修改原始容器'a'。如果您希望避免在返回时进行容器复制所带来的开销，
 *            可以考虑将返回类型修改为'T&'（引用类型），并返回一个引用。
 *
 * @par Examples
 *
 * @code{.cpp}
 *   std::vector<int> numbers = {1, 2, 3, 4, 5};
 *   // Lambda to square each element
 *   inplace_transform(numbers, [](int& n) { n *= n; });
 *   // numbers is now {1, 4, 9, 16, 25}
 * @endcode
 *
 * @see std::for_each
 * @ingroup demo
 * @attention add attention messages here if necessary
 * @bug describe the bug here
 * @pre add the pre-conditions, or status here for applying the function
 * @post add the post-conditions, or status here after applying the function
 * @warning add warning messages here if necessary
 * @exception std::invalid_argument if wrong arguments assigned
 * @todo further optimization if element object is vector like
 * @since 1.0
 * @version 1.0.3 change to left-value argument
 * @version 1.0.4 change to left-value return
 */
template <typename T, typename F>
T& inplace_transform(T& a, F f) {
    for (auto& ele: a) { f(ele); }
    return a;
}



/**
 * @brief docstring of this function should not be included in v1.0 build
 * @since 2.0
 * @deprecated this function will be deprecated in v3.0
 */
auto version_test_func();



class Base {};



class SubBase1 : public Base {};



class SubBase2 : public Base {};



/**
 * @brief class derived demo
 * @note the derivation relationship can be automatically calculated.
 * @ingroup demo
 */
class SubSubBase : public SubBase2 {};
